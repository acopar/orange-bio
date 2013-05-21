from __future__ import absolute_import

import random
import math
from collections import defaultdict

import scipy.stats

import numpy

import Orange, Orange.utils, statc

if __name__ == "__main__":
    __package__ = "Orange.bio"

from .obiGsea import takeClasses
from .obiAssess import pca, PLSCall, corgs_activity_score
from . import obiExpression, obiGene, obiGeneSets, obiGsea, stats

class GeneSetTrans(object):

    __new__ = Orange.utils._orange__new__(object)

    def _mat_ni(self, data):
        """ With cached gene matchers. """
        if data.domain not in self._cache:
            self._cache[data.domain] = mat_ni(data, self.matcher)
        return self._cache[data.domain]

    def _match_instance(self, instance, geneset, takegenes=None):
        """
        Return
            - a gene matcher with the instance as a target
            - { name: attribute indices } of an instance
            - genes names on the data set that were matched by the gene set

        If takegenes is a list of indices, use only genes from
        the gene set with specified indices.
        """
        nm, name_ind = self._mat_ni(instance)
        genes = [ nm.umatch(gene) for gene in geneset ]
        if takegenes:
            genes = [ genes[i] for i in takegenes ]
        return nm, name_ind, genes

    def _match_data(self, data, geneset, odic=False):
        nm, name_ind = self._mat_ni(data)
        genes = [ nm.umatch(gene) for gene in geneset ]
        if odic:
            to_geneset = dict(zip(genes, geneset))
        takegenes = [ i for i,a in enumerate(genes) if a != None ]
        genes = [ genes[i] for i in takegenes ]
        if odic:
            return nm, name_ind, genes, takegenes, to_geneset
        else:
            return nm, name_ind, genes, takegenes

    def __init__(self, matcher=None, gene_sets=None, min_size=3, max_size=1000, min_part=0.1, class_values=None, cv=False):
        self.matcher = matcher
        self.gene_sets = gene_sets
        self.min_size = min_size
        self.max_size = max_size
        self.min_part = min_part
        self.class_values = class_values
        self._cache = {}
        self.cv = cv

    def __call__(self, data, weight_id=None):

        #selection of classes and gene sets
        data = takeClasses(data, classValues=self.class_values)
        nm,_ =  self._mat_ni(data)
        gene_sets = select_genesets(nm, self.gene_sets, self.min_size, self.max_size, self.min_part)

        #build a new domain
        newfeatures = self.build_features(data, gene_sets)
        newdomain = Orange.data.Domain(newfeatures, data.domain.class_var)

        #build a data set with cross validation
        if self.cv == False:
            return Orange.data.Table(newdomain, data)
        else:
            # The domain has the transformer that is build on all samples,
            # while the transformed data table uses cross-validation
            # internally
            if self.cv == True:
                cvi = Orange.data.sample.SubsetIndicesCV(data, 5)
            elif self.cv != False:
                cvi = self.cv(data)
            data_cv = [ [] for _ in range(len(data)) ]
            for f in set(cvi):
                learn = data.select(cvi, f, negate=True)
                test = data.select(cvi, f)
                lf = self.build_features(learn, gene_sets)
                transd = Orange.data.Domain(lf, data.domain.class_var)
                trans_test = Orange.data.Table(transd, test)
                for ex, pos in \
                    zip(trans_test, [ i for i,n in enumerate(cvi) if n == f ]):
                    data_cv[pos] = ex.native(0)
            return Orange.data.Table(newdomain, data_cv)

    def build_features(self, data, gene_sets):
        return [ self.build_feature(data, gs) for gs in gene_sets ]

def normcdf(x, mi, st):
    return 0.5*(2. - stats.erfcc((x - mi)/(st*math.sqrt(2))))

class AT_edelmanParametric(object):

    def __init__(self, **kwargs):
        for a,b in kwargs.items():
            setattr(self, a, b)

    def __call__(self, nval):

        if self.mi1 == None or self.mi2 == None or self.st1 == None or self.st2 == None:
            return 0.0 

        val = nval

        try:
            if val >= self.mi1:
                p1 = 1 - normcdf(val, self.mi1, self.st1)
            else:
                p1 = normcdf(val, self.mi1, self.st1)

            if val >= self.mi2:
                p2 = 1 - normcdf(val, self.mi2, self.st2)
            else:
                p2 = normcdf(val, self.mi2, self.st2)

            #print p1, p2
            return math.log(p1/p2)
        except:
            #print p1, p2, "exception"
            return 0

def estimate_gaussian_per_class(data, i, a=None, b=None, common_if_extreme=False):
    cv = data.domain.class_var

    if a == None: a = cv.values[0]
    if b == None: b = cv.values[1]

    def avWCVal(value):
        return [ex[i].value for ex in data if ex[-1].value == value and not ex[i].isSpecial() ]

    list1 = avWCVal(a)
    list2 = avWCVal(b)

    mi1 = mi2 = st1 = st2 = None

    try:
        mi1 = statc.mean(list1)
        st1 = statc.std(list1)
    except:
        pass

    try:
        mi2 = statc.mean(list2)
        st2 = statc.std(list2)
    except:
        pass

    def extreme():
        return st1 == 0 or st2 == 0
    
    if common_if_extreme and extreme():
        print "extreme", st1, st2,
        st1 = st2 = statc.std(list1 + list2)
        print "new", st1, st2

    return mi1, st1, mi2, st2

class AT_edelmanParametricLearner(object):
    """
    Returns attribute transfromer for Edelman parametric measure for a
    given attribute in the dataset.  Edelman et al, 06. Modified a bit.
    """

    def __init__(self, a=None, b=None):
        """
        a and b are choosen class values.
        """
        self.a = a
        self.b = b

    def __call__(self, i, data):
        cv = data.domain.class_var

        if self.a == None: self.a = cv.values[0]
        if self.b == None: self.b = cv.values[1]

        mi1, st1, mi2, st2 = estimate_gaussian_per_class(data, i, a=self.a, b=self.b)

        return AT_edelmanParametric(mi1=mi1, mi2=mi2, st1=st1, st2=st2)

class AT_loess(object):

    def __init__(self, **kwargs):
        for a,b in kwargs.items():
            setattr(self, a, b)

    def __call__(self, nval):

        val = nval

        def saveplog(a,b):
            try:
                return math.log(a/b)
            except:
                if a < b:
                    return -10
                else:
                    return +10

        try:
            ocene = self.condprob(val)
            if sum(ocene) < 0.01:
                return 0.0
            return saveplog(ocene[0], ocene[1])

        except:
            return 0.0

class AT_loessLearner(object):

    def __call__(self, i, data):
        try:
            ca = Orange.statistics.contingency.VarClass(data.domain.attributes[i], data)
            a =  Orange.statistics.estimate.ConditionalLoess(ca, nPoints=5)
            return AT_loess(condprob=a)
        except:
            return AT_loess(condprob=None)

def nth(l, n):
    return [a[n] for a in l]

class Assess(GeneSetTrans):
    """
    Uses the underlying GSEA code to select genes.
    Takes data and creates attribute transformations.
    """

    def __init__(self, rankingf=None, **kwargs):
        self.rankingf = rankingf
        if self.rankingf == None:
            self.rankingf = AT_edelmanParametricLearner()
        self.example_buffer = {}
        self.attransv = 0
        self.ignore_unmatchable_context = True
        super(Assess, self).__init__(**kwargs)

    def _ordered_and_lcor(self, ex, nm, name_ind, attrans, attransv):
        """ Buffered! It should be computed only once per example. """ 
        #name_ind and nm are always co-created, so I need to have only one as a key
        key = (ex, nm, attransv)
        if key not in self.example_buffer:
            ex_atts = [ at.name for at in ex.domain.attributes ]
            new_atts = [ name_ind[nm.umatch(an)] if nm.umatch(an) != None else (None if self.ignore_unmatchable_context else i)
                for i,an in enumerate(ex_atts) ]

            #new_atts: indices of genes in original data for that sample 
            #POSSIBLE REVERSE IMPLEMENTATION (slightly different
            #for data from different chips):
            #save pairs together and sort (or equiv. dictionary transformation)

            indexes = filter(lambda x: x[0] != None, zip(new_atts, range(len(ex_atts))))

            lcor = [ attrans[index_in_data](ex[index_in_ex].value) 
                for index_in_data, index_in_ex in indexes if
                ex[index_in_ex].value != '?' ]

            indices_to_lcori = dict( (index_in_ex, i) for i,(_, index_in_ex) in enumerate(indexes) 
                if ex[index_in_ex].value != '?')

            #indexes in original lcor, sorted from higher to lower values
            ordered = obiGsea.orderedPointersCorr(lcor)
            rev2 = numpy.argsort(ordered)
            self.example_buffer[key] = lcor, ordered, rev2, indices_to_lcori
        return self.example_buffer[key]

    def build_features(self, data, gene_sets):

        attributes = []

        #attrans: { i_orig: ranking_function }
        attrans = [ self.rankingf(iat, data) for iat, at in enumerate(data.domain.attributes) ]
        attransv = self.attransv
        self.attransv += 1

        nm_all, _ =  self._mat_ni(data)

        for gs in gene_sets:

            at = Orange.feature.Continuous(name=str(gs))

            geneset = list(gs.genes)
            nm, name_ind, genes, takegenes, to_geneset = self._match_data(data, geneset, odic=True)
            takegenes = [ geneset[i] for i in takegenes ]
            genes = set(genes)

            def t(ex, w, takegenes=takegenes, nm=nm, attrans=attrans, attransv=attransv):
                nm2, name_ind2, genes2 = self._match_instance(ex, takegenes)
                lcor, ordered, rev2, indices_to_lcori = \
                    self._ordered_and_lcor(ex, nm, name_ind, attrans, attransv)

           
                #subset = list of indices, lcor = correlations, ordered = order
                #make it compatible with lcor, if some are missing in lcor
                subset = filter(None,
                    [ indices_to_lcori.get(name_ind2[g], None) for g in genes2 ] )

                return obiGsea.enrichmentScoreRanked(subset, lcor, ordered, rev2=rev2)[0] 

            at.get_value_from = t
            attributes.append(at)

        return attributes
   
def setSig_example_geneset(ex, data, no_unknowns, check_same=False):
    """ Gets learning data and example with the same domain, both
    containing only genes from the gene set. """

    distances = [ [], [] ]    

    def pearson(ex1, ex2):
        vals1 = ex1.native(0)[:-1]
        vals2 = ex2.native(0)[:-1]

        if check_same and vals1 == vals2:
            return 10 #they are the same

        #leaves undefined elements out
        if not no_unknowns:
            common = [ True if v1 != "?" and v2 != "?" else False \
                for v1,v2 in zip(vals1,vals2) ]
            vals1 = [ v for v,c in zip(vals1, common) if c ]
            vals2 = [ v for v,c in zip(vals2, common) if c ]

        #statc correlation is from 5-10 times faster than numpy!
        try:
            return statc.pearsonr(vals1, vals2)[0]
        except:
            return numpy.corrcoef([vals1, vals2])[0,1] 
        

    def ttest(ex1, ex2):
        try:
            return stats.lttest_ind(ex1, ex2)[0]
        except:
            return 0.0
    
    #maps class value to its index
    classValueMap = dict( [ (val,i) for i,val in enumerate(data.domain.class_var.values) ])
 
    #create distances to all learning data - save or other class
    for c in data:
        p = pearson(c, ex)
        if p != 10:
             distances[classValueMap[c[-1].value]].append(pearson(c, ex))

    return ttest(distances[0], distances[1])

def mat_ni(data, matcher):
    """ Return (in a tuple):
        - a gene matcher that matches to the attribute names of data
        - a dictionary attribute names -> indices in the data set.
    """
    nm = matcher([at.name for at in data.domain.attributes])
    name_ind = dict((n.name,i) for i,n in enumerate(data.domain.attributes))
    return nm, name_ind

def select_genesets(nm, gene_sets, min_size=3, max_size=1000, min_part=0.1):
    """ Returns a list of gene sets that have sizes in limits """

    def ok_sizes(gs):
        """compares sizes of genesets to limitations"""
        transl = filter(lambda x: x != None, [ nm.umatch(gene) for gene in gs.genes ])
        if len(transl) >= min_size \
            and len(transl) <= max_size \
            and float(len(transl))/len(gs.genes) >= min_part:
            return True
        return False

    return filter(ok_sizes, gene_sets) 

def vou(ex, gn, indices):
    """ returns the value or "?" for the given gene name gn"""
    if gn not in indices:
        return "?"
    else:
        return ex[indices[gn]].value

class SetSig(GeneSetTrans):

    def __init__(self, **kwargs):
        self.no_unknowns = kwargs.pop("no_unknowns", False)
        self.check_same = kwargs.pop("check_same", False)
        super(SetSig, self).__init__(**kwargs)

    def build_feature(self, data, gs):

        at = Orange.feature.Continuous(name=str(gs))
        geneset = list(gs.genes)
        nm, name_ind, genes, takegenes = self._match_data(data, geneset)
        indices = [ name_ind[gene] for gene in genes ]
        takegenes = [ geneset[i] for i in takegenes ]

        def t(ex, w, gs=gs, data=data, indices=indices, takegenes=takegenes):
            nm2, name_ind2, genes2 = self._match_instance(ex, takegenes)

            domain = Orange.data.Domain([data.domain.attributes[i] for i in indices], data.domain.class_var)
            datao = Orange.data.Table(domain, data)
           
            #convert the example to the same domain
            exvalues = [ vou(ex, gn, name_ind2) for gn in genes2 ] + [ "?" ]
            example = Orange.data.Instance(domain, exvalues)

            return setSig_example_geneset(example, datao, self.no_unknowns, check_same=self.check_same) #only this one is setsig specific
     
        at.get_value_from = t
        return at

class ParametrizedTransformation(GeneSetTrans):

    def _get_par(self, datao):
        """ Get parameters for a subset of data, that comprises only the gene set """
        pass
        
    def _use_par(self, ex, constructt):
        pass
    
    def build_feature(self, data, gs):

        at = Orange.feature.Continuous(name=str(gs))

        geneset = list(gs.genes)
        nm, name_ind, genes, takegenes = self._match_data(data, geneset)
        domain = Orange.data.Domain([data.domain.attributes[name_ind[gene]] for gene in genes], data.domain.class_var)
        datao = Orange.data.Table(domain, data)
        takegenes = [ geneset[i] for i in takegenes ]

        constructt = self._get_par(datao)

        def t(ex, w, constructt=constructt, takegenes=takegenes, domain=domain):
            nm2, name_ind2, genes2 = self._match_instance(ex, takegenes)
          
            #convert the example to the same domain
            exvalues = [ vou(ex, gn, name_ind2) for gn in genes2 ] + [ "?" ]
            ex = Orange.data.Instance(domain, exvalues)

            return self._use_par(ex, constructt)
        
        at.get_value_from = t
        at.dbg = constructt #for debugging
        
        return at

class PLS(ParametrizedTransformation):

    def _get_par(self, datao):
        return PLSCall(datao, nc=1, y=[datao.domain.class_var])
        
    def _use_par(self, ex, constructt):
        ex = [ ex[i].value for i in range(len(ex.domain.attributes)) ]
        xmean, W, P, _ = constructt
        ex = ex - xmean # same input transformation

        nc = W.shape[1]

        TR = numpy.empty((1, nc))
        XR = ex

        dot = numpy.dot

        for i in range(nc):
           t = dot(XR, W[:,i].T)
           XR = XR - t*numpy.array([P[:,i]])
           TR[:,i] = t

        return TR[0][0]
        
class PCA(ParametrizedTransformation):

    def _get_par(self, datao):
        return pca(datao)

    def _use_par(self, arr, constructt):
        arr = [ arr[i].value for i in range(len(arr.domain.attributes)) ]
        evals, evect, xmean = constructt

        arr = arr - xmean # same input transformation - a row in a matrix
        ev0 = evect[0] #this is a row in a matrix - do a dot product
        a = numpy.dot(arr, ev0)

        return a

class SimpleFun(GeneSetTrans):

    def build_feature(self, data, gs):

        at = Orange.feature.Continuous(name=str(gs))

        def t(ex, w, gs=gs):
            geneset = list(gs.genes)
            nm2, name_ind2, genes2 = self._match_instance(ex, geneset)
           
            exvalues = [ vou(ex, gn, name_ind2) for gn in genes2 ] + [ "?" ]
            exvalues = filter(lambda x: x != "?", exvalues)

            return self.fn(exvalues)
     
        at.get_value_from = t
        return at

class Mean(SimpleFun):

    def __init__(self, **kwargs):
       self.fn = numpy.mean
       super(Mean, self).__init__(**kwargs)

class Median(SimpleFun):

    def __init__(self, **kwargs):
       self.fn = numpy.median
       super(Median, self).__init__(**kwargs)

class GSA(GeneSetTrans):

    def build_features(self, data, gene_sets):

        attributes = []

        def tscorec(data, at, cache=None):
            ma = obiExpression.MA_t_test()(at,data)
            return ma

        tscores = [ tscorec(data, at) for at in data.domain.attributes ]

        def to_z_score(t):
            return float(scipy.stats.norm.ppf(scipy.stats.t.cdf(t, len(data)-2)))

        zscores = map(to_z_score, tscores)

        for gs in gene_sets:

            at = Orange.feature.Continuous(name=str(gs))

            geneset = list(gs.genes)
            nm, name_ind, genes, takegenes, to_geneset = self._match_data(data, geneset, odic=True)
            #take each gene only once
            genes = set(genes)

            D = numpy.mean([max(zscores[name_ind[g]],0) for g in genes]) \
                + numpy.mean([min(zscores[name_ind[g]],0) for g in genes])

            if D >= 0:
                consider_genes = [ to_geneset[g] for g in genes if zscores[name_ind[g]] > 0.0 ]
            else:
                consider_genes = [ to_geneset[g] for g in genes if zscores[name_ind[g]] < 0.0 ]

            def t(ex, w, consider_genes=consider_genes):
                nm2, name_ind2, genes2 = self._match_instance(ex, consider_genes)
              
                #convert the example to the same domain
                exvalues = [ vou(ex, gn, name_ind2) for gn in genes2 ] + [ "?" ]
                exvalues = filter(lambda x: x != "?", exvalues)
              
                return numpy.mean(exvalues)

            at.get_value_from = t
            attributes.append(at)

        return attributes

def tscorec(data, at, cache=None):
    """ Cached attribute  tscore calculation """
    if cache != None and at in cache: return cache[at]
    ma = obiExpression.MA_t_test()(at,data)
    if cache != None: cache[at] = ma
    return ma

def nth(l, n):
    return [a[n] for a in l]

def compute_corg(data, inds, tscorecache):
    """
    Compute CORG for this geneset specified with gene inds
    in the example table. Output is the list of gene inds
    in CORG.

    """
    #order member genes by their t-scores: decreasing, if av(t-score) >= 0,
    #else increasing
    tscores = [ tscorec(data, at, tscorecache) for at in inds ]
    sortedinds = nth(sorted(zip(inds,tscores), key=lambda x: x[1], \
        reverse=numpy.mean(tscores) >= 0), 0)

    def S(corg):
        """ Activity score separation - S(G) in 
        the article """
        asv = Orange.feature.Continuous(name='AS')
        asv.getValueFrom = lambda ex,rw: Orange.data.Value(asv, corgs_activity_score(ex, corg))
        data2 = Orange.data.Table(Orange.data.Domain([asv], data.domain.classVar), data)
        return abs(tscorec(data2, 0)) #FIXME absolute - nothing in the article abs()
            
    #greedily find CORGS procing the best separation
    g = S(sortedinds[:1])
    bg = 1
    for a in range(2, len(sortedinds)+1):
        tg = S(sortedinds[:a])
        if tg > g: #improvement
            g = tg
            bg = a
        else:
            break
        
    return sortedinds[:bg] #FIXED - one too many was taken

class CORGs(ParametrizedTransformation):
    """
    WARNING: input has to be z_ij table! each gene needs to be normalized
    (mean=0, stdev=1) for all samples.
    """

    def __call__(self, *args, **kwargs):
        self.tscorecache = {} #reset a cache
        return super(CORGs, self).__call__(*args, **kwargs)

    def build_feature(self, data, gs):

        at = Orange.feature.Continuous(name=str(gs))
        geneset = list(gs.genes)

        nm, name_ind, genes, takegenes, to_geneset = self._match_data(data, geneset, odic=True)
        indices = compute_corg(data, [ name_ind[g] for g in genes ], self.tscorecache)

        ind_names = dict( (a,b) for b,a in name_ind.items() )
        selected_genes = sorted(set([to_geneset[ind_names[i]] for i in indices]))
            
        def t(ex, w, corg=selected_genes): #copy od the data
            nm2, name_ind2, genes2 = self._match_instance(ex, corg, None)
            exvalues = [ vou(ex, gn, name_ind2) for gn in genes2 ]
            return sum(v if v != '?' else 0.0 for v in exvalues)/len(corg)**0.5
     
        at.get_value_from = t
        return at

def compute_llr(data, inds, cache):
    """
    Compute CORG for this geneset specified with gene inds
    in the example table. Output is the list of gene inds
    in CORG.
    """
    def gaussianc(data, at, cache=None):
        """ Cached attribute  tscore calculation """
        if cache != None and at in cache: return cache[at]
        ma = estimate_gaussian_per_class(data, at, common_if_extreme=True)
        if cache != None: cache[at] = ma
        return ma

    gf = [ gaussianc(data, at, cache) for at in inds ]
    return gf

""" To avoid scipy overhead """
from math import pi
_norm_pdf_C = math.sqrt(2*pi)
_norm_pdf_logC = math.log(_norm_pdf_C)
def _norm_logpdf(x, mi, std):
    return -(x-mi)**2 / (2.0*std**2) - _norm_pdf_logC - math.log(std)

def _llrlogratio(v, mi1, std1, mi2, std2):
    if mi1 == None or std1 == None or mi2 == None or std2 == None:
        return 0. #problem with estimation
    #lpdf1 = scipy.stats.norm.logpdf(v, mi1, std1)
    #lpdf2 = scipy.stats.norm.logpdf(v, mi2, std2)
    lpdf1 = _norm_logpdf(v, mi1, std1) #avoids scipy's overhead
    lpdf2 = _norm_logpdf(v, mi2, std2)
    r = lpdf1 - lpdf2
    return r

class LLR(ParametrizedTransformation):
    """ 
    From Su et al: Accurate and Reliable Cancer Classification Base
    on Probalistic Inference of Pathway Activity. Plos One, 2009.
    """

    def __init__(self, **kwargs):
        self.normalize = kwargs.pop("normalize", False) #normalize final results
        super(LLR, self).__init__(**kwargs)

    def __call__(self, *args, **kwargs):
        self._gauss_cache = {} #caching of gaussian estimates
        self._normalizec = {}
        return super(LLR, self).__call__(*args, **kwargs)

    def build_feature(self, data, gs):

        at = Orange.feature.Continuous(name=str(gs))
        geneset = list(gs.genes)

        nm, name_ind, genes, takegenes, to_geneset = self._match_data(data, geneset, odic=True)

        gsi = [ name_ind[g] for g in genes ]
        gausse = compute_llr(data, gsi, self._gauss_cache)
        genes_gs = [ to_geneset[g] for g in genes ]

        if self.normalize: # per (3) in the paper
            #compute log ratios for all samples and genes from this gene set
            for i, gene_gs, g in zip(gsi, genes_gs, gausse):
                if gene_gs not in self._normalizec: #skip if computed already
                    r = [ _llrlogratio(ex[i].value, *g) for ex in data ]
                    self._normalizec[gene_gs] = (statc.mean(r), statc.std(r))

        def t(ex, w, genes_gs=genes_gs, gausse=gausse, normalizec=self._normalizec):
            nm2, name_ind2, genes2 = self._match_instance(ex, genes_gs, None)
            gsvalues = [ vou(ex, gn, name_ind2) for gn in genes2 ]

            vals = [ _llrlogratio(v, *g) if v != "?" else 0.0 for v,g in zip(gsvalues, gausse) ]

            if len(normalizec): #normalize according to (3)
                vals2 = []
                for v,g in zip(vals, genes_gs):
                    m,s = self._normalizec[g]
                    vals2.append((v-m)/s)
                vals = vals2
            
            return sum(vals)

     
        at.get_value_from = t
        return at

def estimate_linear_fit(data, i):
    """
    Chen et 2008 write about t-score of the least square fit in the
    original article, but here we can use just the t-test, because the
    t-scores obtained are exactly the same (the authors used the
    the more general version as they supported continous outcomes).
    """
    
    """
    #implementation that could also support continous outcomes
    x = numpy.array([ ex[i].value for ex in data ])
    y = numpy.array([ int(ex[-1]) for ex in data ]) #here classes are 0 and 1
    ret = scipy.stats.linregress(x,y)
    b = ret[0]
    seb = ret[4]
    return b/seb
    """
    """
    #per mathword.wolfram.com - results are the same
    c = numpy.cov(x,y)
    n = len(x)
    b = c[0,1]/c[0,0] #the same result as from li
    s = math.sqrt((c[1,1]*n - b*c[0,1]*n)/(n-2))
    seb = s/math.sqrt(c[0,0]*n)
    return b/seb
    """
    return obiExpression.MA_t_test()(i, data)


class SPCA(ParametrizedTransformation):
    """ Per Chen et al. Supervised principal component analysis for
    gene set enrichment of microarray data with continuous or survival
    outcomes. Bioinformatics, 2008.  """

    def __init__(self, **kwargs):
        self.threshold = kwargs.pop("threshold", None)
        self.top = kwargs.pop("top", None)
        self.atleast = kwargs.pop("atleast", 0)
        super(SPCA, self).__init__(**kwargs)

    def _get_par(self, datao):
        scores = [ estimate_linear_fit(datao, a) for a in range(len(datao.domain.attributes)) ]
        scores = list(enumerate(map(abs, scores)))
        select = None
        if self.threshold is not None:
            select = [ i for i,s in scores if s > self.threshold ]
        elif self.top is not None:
            select = nth(sorted(scores, key=lambda x: -x[1])[:self.top], 0)

        if len(select) < self.atleast:
            select = nth(sorted(scores, key=lambda x: -x[1])[:self.atleast], 0)

        if select == None:
            somethingWrongWithSelection

        doms = Orange.data.Domain([ datao.domain.attributes[i] for i in select ], datao.domain.class_var)
        datas = Orange.data.Table(doms, datao)

        if len(select) == 0:
            return select, None
        else:
            return set(select), pca(datas)

    def _use_par(self, arr, constructt):
        select, constructt = constructt

        if len(select) == 0:
            return 0.

        arr = [ arr[i].value for i in range(len(arr.domain.attributes)) 
            if i in select ]

        evals, evect, xmean = constructt

        arr = arr - xmean # same input transformation - a row in a matrix
        ev0 = evect[0] #this is a row in a matrix - do a dot product
        a = numpy.dot(arr, ev0)

        return a

def _shuffleClass(data, rand):
    """ Destructive! """
    locations = range(len(data))
    rand.shuffle(locations)
    attribute = -1
    l = [None]*len(data)
    for i in range(len(data)):
        l[locations[i]] = data[i][attribute]
    for i in range(len(data)):
        data[i][attribute] = l[i]

class SPCA_ttperm(SPCA):
    """ Set threshold with a permutation test. """

    def __init__(self, **kwargs):
        self.pval = kwargs.pop("pval", 0.01) #target p-value
        self.perm = kwargs.pop("perm", 100) #number of class permutation
        self.sperm = kwargs.pop("sperm", 100) #sampled attributes per permutation
        super(SPCA_ttperm, self).__init__(**kwargs)

    def __call__(self, data, *args, **kwargs):
        joined = []
        rand = random.Random(0)
        nat = len(data.domain.attributes)

        datap = Orange.data.Table(data.domain, data)

        for p in range(self.perm):
            _shuffleClass(datap, rand)
            if self.sperm is not None:
                ti = rand.sample(xrange(nat), self.sperm)
            else:
                ti = range(nat)
            joined.extend([ obiExpression.MA_t_test()(i, datap) 
                for i in ti ])

        joined = map(abs, joined)
        joined.sort(reverse=True)

        t = joined[int(self.pval*len(joined))]

        self.threshold = t
        return super(SPCA_ttperm, self).__call__(data, *args, **kwargs)
    

if __name__ == "__main__":

    data = Orange.data.Table("iris")

    gsets = obiGeneSets.collections({
        #"ALL": ['sepal length', 'sepal width', 'petal length', 'petal width'],
        "f3": ['sepal length', 'sepal width', 'petal length'],
        "l3": ['sepal width', 'petal length', 'petal width'],
        })
    matcher = obiGene.matcher([])
    choosen_cv = ["Iris-setosa", "Iris-versicolor"]

    """
    data = Orange.data.Table("DLBCL_200a")
    gsets = obiGeneSets.collections((("KEGG",),"9606"))
    matcher = obiGene.matcher([obiGene.GMKEGG("hsa")])
    choosen_cv = None
    """

    def to_old_dic(d, data):
        ar = defaultdict(list)
        for ex1 in data:
            ex = d(ex1)
            for a,x in zip(d.attributes, ex):
                ar[a.name].append(x.value)
        return ar

    def pp2(ar):
        ol =  sorted(ar.items())
        print '\n'.join([ a + ": " +str(b) for a,b in ol])

    ass = SPCA(data, matcher=matcher, gene_sets=gsets, class_values=choosen_cv, min_part=0.0, top=0)
    ar = to_old_dic(ass.domain, data[:5])
    pp2(ar)
