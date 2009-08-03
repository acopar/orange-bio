from __future__ import division
import obiGO, obiProb
import orange

data = orange.ExampleTable("../../../../doc/datasets/brown-selected.tab")

ontology = obiGO.Ontology()
annotations = obiGO.Annotations("yeast", ontology=ontology)

cluster_genes = [str(ex["gene"]) for ex in data if ex.getclass() == "Resp"]

gg = dict([(b, a) for a, b in annotations.GetGeneNamesTranslator(cluster_genes).items()])
cluster_genes = [gg.get(name, name) for name in cluster_genes]
gg = dict([(ann.DB_Object_Symbol, ann.DB_Object_ID) for ann in annotations])
cluster_genes = [gg.get(name, name) for name in cluster_genes]
cluster_genes = cluster_genes[:10]
reference_genes = annotations.geneNames

david_date = "August 3, 2009"

david_results_bp = """Category	Term	Count	%	PValue	Genes	List Total	Pop Hits	Pop Total	Fold Enrichment	Bonferroni	Benjamini	FDR
GOTERM_BP_ALL	GO:0015992~proton transport	8	57.14%	1.3041103299910861E-11	S000003882, S000002706, S000000195, S000005999, S000000195, S000005999, S000003882, S000005999, 	14	53	5164	55.676549865229106	3.115524416230642E-8	2.077016336698989E-9	2.2887058914733416E-8
GOTERM_BP_ALL	GO:0015986~ATP synthesis coupled proton transport	8	57.14%	2.3084091771234847E-12	S000003882, S000002706, S000000195, S000005999, S000000195, S000005999, S000003882, S000005999, 	14	42	5164	70.25850340136054	5.514709577880694E-9	1.8382365629676656E-9	4.051181612396704E-9
GOTERM_BP_ALL	GO:0044249~cellular biosynthetic process	8	57.14%	0.0026654367159150284	S000003882, S000002706, S000000195, S000005999, S000000195, S000005999, S000003882, S000005999, 	14	878	5164	3.360885128538887	0.9982984740500304	0.14734967010922517	4.5760545698257165
GOTERM_BP_ALL	GO:0015672~monovalent inorganic cation transport	8	57.14%	6.501499399871959E-11	S000003882, S000002706, S000000195, S000005999, S000000195, S000005999, S000003882, S000005999, 	14	66	5164	44.70995670995671	1.5532080710478624E-7	8.62893434483425E-9	1.1410075106965678E-7
GOTERM_BP_ALL	GO:0006818~hydrogen transport	8	57.14%	1.3041103299910861E-11	S000003882, S000002706, S000000195, S000005999, S000000195, S000005999, S000003882, S000005999, 	14	53	5164	55.676549865229106	3.115524416230642E-8	2.077016336698989E-9	2.2887058914733416E-8
GOTERM_BP_ALL	GO:0051234~establishment of localization	9	64.29%	0.004162009675774264	S000003882, S000002706, S000000195, S000005999, S000000195, S000005999, S000003882, S000005999, S000003439, 	14	1235	5164	2.6880277617119726	0.9999529260234311	0.2111926048706756	7.058073886583582
GOTERM_BP_ALL	GO:0006812~cation transport	8	57.14%	3.2348983576564486E-8	S000003882, S000002706, S000000195, S000005999, S000000195, S000005999, S000003882, S000005999, 	14	158	5164	18.67631103074141	7.727873692198184E-5	2.5760541179087326E-6	5.677217334021378E-5
GOTERM_BP_ALL	GO:0009165~nucleotide biosynthetic process	8	57.14%	2.884205297126469E-9	S000003882, S000002706, S000000195, S000005999, S000000195, S000005999, S000003882, S000005999, 	14	112	5164	26.346938775510203	6.8903427785649285E-6	2.460844882312685E-7	5.061755459223605E-6
GOTERM_BP_ALL	GO:0006811~ion transport	8	57.14%	9.322978491193589E-8	S000003882, S000002706, S000000195, S000005999, S000000195, S000005999, S000003882, S000005999, 	14	184	5164	16.03726708074534	2.2270116490286096E-4	6.960162230784661E-6	1.6361734598291378E-4
GOTERM_BP_ALL	GO:0006810~transport	9	64.29%	0.003689044915217824	S000003882, S000002706, S000000195, S000005999, S000000195, S000005999, S000003882, S000005999, S000003439, 	14	1213	5164	2.7367801201271935	0.9998536375393898	0.19374226311229126	6.280333887049161
GOTERM_BP_ALL	GO:0009058~biosynthetic process	8	57.14%	0.012969438334012132	S000003882, S000002706, S000000195, S000005999, S000000195, S000005999, S000003882, S000005999, 	14	1153	5164	2.5592863337876346	0.9999999999999715	0.49994490614887377	20.47521247842694
GOTERM_BP_ALL	GO:0042775~organelle ATP synthesis coupled electron transport	3	21.43%	0.001698878089256512	S000003155, S000004997, S000004387, 	14	25	5164	44.26285714285714	0.9827866703378599	0.098914987364349	2.93996869915667
GOTERM_BP_ALL	GO:0006164~purine nucleotide biosynthetic process	8	57.14%	2.1784520172080657E-10	S000003882, S000002706, S000000195, S000005999, S000000195, S000005999, S000003882, S000005999, 	14	78	5164	37.83150183150183	5.20432014816663E-7	2.1684672724120446E-8	3.8231643406660965E-7
GOTERM_BP_ALL	GO:0042773~ATP synthesis coupled electron transport	3	21.43%	0.001698878089256512	S000003155, S000004997, S000004387, 	14	25	5164	44.26285714285714	0.9827866703378599	0.098914987364349	2.93996869915667
GOTERM_BP_ALL	GO:0006163~purine nucleotide metabolic process	8	57.14%	2.8583856087082035E-10	S000003882, S000002706, S000000195, S000005999, S000000195, S000005999, S000003882, S000005999, 	14	81	5164	36.430335097001766	6.828681227144529E-7	2.6264167174439024E-8	5.016442483629646E-7
GOTERM_BP_ALL	GO:0007571~age-dependent general metabolic decline	2	14.29%	0.02491247592376542	S000003882, S000003882, 	14	10	5164	73.77142857142856	1.0	0.7226114630464955	35.77322472636095
GOTERM_BP_ALL	GO:0009152~purine ribonucleotide biosynthetic process	8	57.14%	1.3504564734308501E-10	S000003882, S000002706, S000000195, S000005999, S000000195, S000005999, S000003882, S000005999, 	14	73	5164	40.422700587084144	3.226239850828705E-7	1.5363049277183904E-8	2.3700393869674485E-7
GOTERM_BP_ALL	GO:0006796~phosphate metabolic process	11	78.57%	6.609360672311857E-11	S000003882, S000002706, S000003155, S000000195, S000005999, S000004997, S000000195, S000005999, S000003882, S000005999, S000004387, 	14	290	5164	13.991133004926107	1.578975383775827E-7	8.310397370259182E-9	1.1599365912218218E-7
GOTERM_BP_ALL	GO:0009260~ribonucleotide biosynthetic process	8	57.14%	1.9849931357144687E-10	S000003882, S000002706, S000000195, S000005999, S000000195, S000005999, S000003882, S000005999, 	14	77	5164	38.32282003710575	4.7421478244213944E-7	2.061803872077661E-8	3.4836461493270576E-7
GOTERM_BP_ALL	GO:0006793~phosphorus metabolic process	11	78.57%	6.609360672311857E-11	S000003882, S000002706, S000003155, S000000195, S000005999, S000004997, S000000195, S000005999, S000003882, S000005999, S000004387, 	14	290	5164	13.991133004926107	1.578975383775827E-7	8.310397370259182E-9	1.1599365912218218E-7
GOTERM_BP_ALL	GO:0009150~purine ribonucleotide metabolic process	8	57.14%	1.6417078391964835E-10	S000003882, S000002706, S000000195, S000005999, S000000195, S000005999, S000003882, S000005999, 	14	75	5164	39.3447619047619	3.922039358839058E-7	1.7827454956709232E-8	2.8811831809250066E-7
GOTERM_BP_ALL	GO:0009259~ribonucleotide metabolic process	8	57.14%	2.3877846642490237E-10	S000003882, S000002706, S000000195, S000005999, S000000195, S000005999, S000003882, S000005999, 	14	79	5164	37.35262206148282	5.704415340090918E-7	2.2817667644225992E-8	4.1905411363174494E-7
GOTERM_BP_ALL	GO:0051188~cofactor biosynthetic process	8	57.14%	3.4773191839524677E-9	S000003882, S000002706, S000000195, S000005999, S000000195, S000005999, S000003882, S000005999, 	14	115	5164	25.659627329192546	8.307281102348796E-6	2.864591178708409E-7	6.102665184304357E-6
GOTERM_BP_ALL	GO:0046034~ATP metabolic process	8	57.14%	3.870915746856979E-12	S000003882, S000002706, S000000195, S000005999, S000000195, S000005999, S000003882, S000005999, 	14	45	5164	65.57460317460317	9.247588694805131E-9	1.5412647824675219E-9	6.793399176530102E-9
GOTERM_BP_ALL	GO:0006123~mitochondrial electron transport, cytochrome c to oxygen	3	21.43%	2.6032148376007355E-4	S000003155, S000004997, S000004387, 	14	10	5164	110.65714285714284	0.46312446340401836	0.016670004919741466	0.4558791472939139
GOTERM_BP_ALL	GO:0051186~cofactor metabolic process	8	57.14%	3.7293039277677224E-7	S000003882, S000002706, S000000195, S000005999, S000000195, S000005999, S000003882, S000005999, 	14	225	5164	13.114920634920635	8.905341134267664E-4	2.5454843862848797E-5	6.544876183900428E-4
GOTERM_BP_ALL	GO:0009145~purine nucleoside triphosphate biosynthetic process	8	57.14%	5.353761737671291E-12	S000003882, S000002706, S000000195, S000005999, S000000195, S000005999, S000003882, S000005999, 	14	47	5164	62.78419452887537	1.2790030923248707E-8	1.4211145593634456E-9	9.39572863956073E-9
GOTERM_BP_ALL	GO:0009144~purine nucleoside triphosphate metabolic process	8	57.14%	6.261365320746103E-12	S000003882, S000002706, S000000195, S000005999, S000000195, S000005999, S000003882, S000005999, 	14	48	5164	61.476190476190474	1.4958304817014323E-8	1.4958304594969718E-9	1.0988576715220688E-8
GOTERM_BP_ALL	GO:0006119~oxidative phosphorylation	11	78.57%	2.1818706134527815E-17	S000003882, S000002706, S000003155, S000000195, S000005999, S000004997, S000000195, S000005999, S000003882, S000005999, S000004387, 	14	68	5164	59.668067226890756	5.212488895538695E-14	5.212488895538695E-14	3.829164197571297E-14
GOTERM_BP_ALL	GO:0008152~metabolic process	14	100.00%	0.019621353851322847	S000004997, S000004387, S000003159, S000003439, S000003882, S000002706, S000000195, S000003155, S000005999, S000000195, S000005999, S000003882, S000004028, S000005999, 	14	3818	5164	1.352540597171294	1.0	0.6426933342222417	29.374312706476815
GOTERM_BP_ALL	GO:0009142~nucleoside triphosphate biosynthetic process	8	57.14%	1.1330305911809188E-11	S000003882, S000002706, S000000195, S000005999, S000000195, S000005999, S000003882, S000005999, 	14	52	5164	56.747252747252745	2.706801482954546E-8	1.933429638611983E-9	1.9884527358016157E-8
GOTERM_BP_ALL	GO:0006118~electron transport	6	42.86%	1.1045195750922386E-5	S000003155, S000004997, S000004028, S000004387, S000003439, S000003159, 	14	132	5164	16.766233766233768	0.026042020409655975	7.327069494768024E-4	0.019382452143623663
GOTERM_BP_ALL	GO:0051179~localization	9	64.29%	0.005041519242062774	S000003882, S000002706, S000000195, S000005999, S000000195, S000005999, S000003882, S000005999, S000003439, 	14	1271	5164	2.611891648870406	0.999994297765288	0.23999017511150011	8.48817753150758
GOTERM_BP_ALL	GO:0009141~nucleoside triphosphate metabolic process	8	57.14%	1.7133267420743854E-11	S000003882, S000002706, S000000195, S000005999, S000000195, S000005999, S000003882, S000005999, 	14	55	5164	53.65194805194805	4.093144034822416E-8	2.40773179172038E-9	3.006878079858666E-8
GOTERM_BP_ALL	GO:0006754~ATP biosynthetic process	8	57.14%	3.2721626944045396E-12	S000003882, S000002706, S000000195, S000005999, S000000195, S000005999, S000003882, S000005999, 	14	44	5164	67.06493506493506	7.817191005621282E-9	1.954297723649745E-9	5.742617492643376E-9
GOTERM_BP_ALL	GO:0006753~nucleoside phosphate metabolic process	8	57.14%	3.2721626944045396E-12	S000003882, S000002706, S000000195, S000005999, S000000195, S000005999, S000003882, S000005999, 	14	44	5164	67.06493506493506	7.817191005621282E-9	1.954297723649745E-9	5.742617492643376E-9
GOTERM_BP_ALL	GO:0055086~nucleobase, nucleoside and nucleotide metabolic process	8	57.14%	1.7766800583227095E-7	S000003882, S000002706, S000000195, S000005999, S000000195, S000005999, S000003882, S000005999, 	14	202	5164	14.608203677510607	4.2435883801938967E-4	1.248371336348697E-5	3.1180536678165893E-4
GOTERM_BP_ALL	GO:0006091~generation of precursor metabolites and energy	14	100.00%	1.7111195002613388E-16	S000004997, S000004387, S000003159, S000003439, S000003882, S000002706, S000000195, S000003155, S000005999, S000000195, S000005999, S000003882, S000004028, S000005999, 	14	322	5164	16.03726708074534	5.304645611658998E-13	2.652322805829499E-13	3.885780586188048E-13
GOTERM_BP_ALL	GO:0009117~nucleotide metabolic process	8	57.14%	5.840328188592497E-8	S000003882, S000002706, S000000195, S000005999, S000000195, S000005999, S000003882, S000005999, 	14	172	5164	17.156146179401993	1.3951571125714324E-4	4.500810660945653E-6	1.0249720883148683E-4
GOTERM_BP_ALL	GO:0006732~coenzyme metabolic process	8	57.14%	1.081918945782046E-7	S000003882, S000002706, S000000195, S000005999, S000000195, S000005999, S000003882, S000005999, 	14	188	5164	15.696048632218842	2.584370494638222E-4	7.832407207586378E-6	1.8987567623751644E-4
GOTERM_BP_ALL	GO:0009108~coenzyme biosynthetic process	8	57.14%	1.3849814685789753E-9	S000003882, S000002706, S000000195, S000005999, S000000195, S000005999, S000003882, S000005999, 	14	101	5164	29.216407355021214	3.3087152432331735E-6	1.2254520420640347E-7	2.430630552385793E-6
GOTERM_BP_ALL	GO:0001321~age-dependent general metabolic decline during replicative cell aging	2	14.29%	0.005029005617493512	S000003882, S000003882, 	14	2	5164	368.85714285714283	0.9999941238340904	0.2442972120915523	8.467976406149823
GOTERM_BP_ALL	GO:0016310~phosphorylation	11	78.57%	4.944705485834868E-12	S000003882, S000002706, S000003155, S000000195, S000005999, S000004997, S000000195, S000005999, S000003882, S000005999, S000004387, 	14	224	5164	18.113520408163268	1.181291520158112E-8	1.6875593145115886E-9	8.677925045219581E-9
GOTERM_BP_ALL	GO:0009206~purine ribonucleoside triphosphate biosynthetic process	8	57.14%	5.353761737671291E-12	S000003882, S000002706, S000000195, S000005999, S000000195, S000005999, S000003882, S000005999, 	14	47	5164	62.78419452887537	1.2790030923248707E-8	1.4211145593634456E-9	9.39572863956073E-9
GOTERM_BP_ALL	GO:0009205~purine ribonucleoside triphosphate metabolic process	8	57.14%	6.261365320746103E-12	S000003882, S000002706, S000000195, S000005999, S000000195, S000005999, S000003882, S000005999, 	14	48	5164	61.476190476190474	1.4958304817014323E-8	1.4958304594969718E-9	1.0988576715220688E-8
GOTERM_BP_ALL	GO:0009201~ribonucleoside triphosphate biosynthetic process	8	57.14%	8.476650445053009E-12	S000003882, S000002706, S000000195, S000005999, S000000195, S000005999, S000003882, S000005999, 	14	50	5164	59.01714285714286	2.0250749632744203E-8	1.68756253415836E-9	1.4876466725155524E-8
GOTERM_BP_ALL	GO:0009199~ribonucleoside triphosphate metabolic process	8	57.14%	9.815138922270817E-12	S000003882, S000002706, S000000195, S000005999, S000000195, S000005999, S000003882, S000005999, 	14	51	5164	57.85994397759104	2.3448390007452247E-8	1.803722282645026E-9	1.7225498805117923E-8
"""

david_results_cc = """Category	Term	Count	%	PValue	Genes	List Total	Pop Hits	Pop Total	Fold Enrichment	Bonferroni	Benjamini	FDR
GOTERM_CC_ALL	GO:0044444~cytoplasmic part	12	85.71%	0.006088819536079676	S000003882, S000002706, S000003155, S000000195, S000005999, S000004997, S000005999, S000003882, S000004028, S000004387, S000003439, S000003159, 	14	2641	5632	1.827879050143344	0.9814660869691836	0.13275524314652598	8.72075140466545
GOTERM_CC_ALL	GO:0031090~organelle membrane	10	71.43%	3.029187860465467E-6	S000003882, S000002706, S000003155, S000000195, S000005999, S000004997, S000003882, S000004028, S000004387, S000003159, 	14	700	5632	5.746938775510205	0.0019761075921682636	1.0410314240905105E-4	0.004525594357451812
GOTERM_CC_ALL	GO:0031975~envelope	10	71.43%	4.78624197919905E-8	S000003882, S000002706, S000003155, S000000195, S000005999, S000004997, S000003882, S000004028, S000004387, S000003159, 	14	434	5632	9.269256089532588	3.125367247458488E-5	2.8412833162905216E-6	7.15077466795222E-5
GOTERM_CC_ALL	GO:0043234~protein complex	13	92.86%	2.603956264388198E-7	S000004997, S000004387, S000003159, S000003882, S000002706, S000000195, S000003155, S000005999, S000000195, S000005999, S000003882, S000005999, S000004028, 	14	1316	5632	3.973947025618758	1.7002391047071796E-4	1.2145523826445626E-5	3.890375158688286E-4
GOTERM_CC_ALL	GO:0044429~mitochondrial part	10	71.43%	1.0957063379250622E-7	S000003882, S000002706, S000003155, S000000195, S000005999, S000004997, S000003882, S000004028, S000004387, S000003159, 	14	477	5632	8.433662773285414	7.154706817014134E-5	5.503802375850242E-6	1.6370141305843688E-4
GOTERM_CC_ALL	GO:0031967~organelle envelope	10	71.43%	4.503200851575421E-8	S000003882, S000002706, S000003155, S000000195, S000005999, S000004997, S000003882, S000004028, S000004387, S000003159, 	14	431	5632	9.333775273450447	2.9405469906707005E-5	2.9405859021114367E-6	6.727903724135231E-5
GOTERM_CC_ALL	GO:0005754~mitochondrial proton-transporting ATP synthase, catalytic core	3	21.43%	1.4737764835078688E-5	S000003882, S000000195, S000003882, 	14	3	5632	402.2857142857143	0.009577670489531065	4.1833992163242684E-4	0.0220163639806481
GOTERM_CC_ALL	GO:0031966~mitochondrial membrane	10	71.43%	1.080240517000826E-9	S000003882, S000002706, S000003155, S000000195, S000005999, S000004997, S000003882, S000004028, S000004387, S000003159, 	14	283	5632	14.215042907622413	7.05396839717487E-7	1.4107940771168614E-7	1.613909073050479E-6
GOTERM_CC_ALL	GO:0005753~mitochondrial proton-transporting ATP synthase complex	5	35.71%	9.998508143708598E-8	S000003882, S000002706, S000000195, S000005999, S000003882, 	14	21	5632	95.78231292517006	6.528813007933287E-5	5.440840318726714E-6	1.493803553298534E-4
GOTERM_CC_ALL	GO:0005751~mitochondrial respiratory chain complex IV	5	35.71%	8.365377472985592E-9	S000003155, S000004997, S000004028, S000004387, S000003159, 	14	12	5632	167.61904761904765	5.462576611603431E-6	6.82823708353375E-7	1.2498103152402962E-5
GOTERM_CC_ALL	GO:0044425~membrane part	13	92.86%	4.362609746181852E-7	S000004997, S000004387, S000003159, S000003882, S000002706, S000000195, S000003155, S000005999, S000000195, S000005999, S000003882, S000005999, S000004028, 	14	1375	5632	3.8034285714285714	2.848379045127247E-4	1.8991718223948517E-5	6.517839032826878E-4
GOTERM_CC_ALL	GO:0016469~proton-transporting two-sector ATPase complex	8	57.14%	2.9258138389520786E-12	S000003882, S000002706, S000000195, S000005999, S000000195, S000005999, S000003882, S000005999, 	14	47	5632	68.4741641337386	1.910528291126923E-9	9.552640900523102E-10	4.3711811947844126E-9
GOTERM_CC_ALL	GO:0005746~mitochondrial respiratory chain	5	35.71%	9.653058317842064E-7	S000003155, S000004997, S000004028, S000004387, S000003159, 	14	36	5632	55.87301587301587	6.30146386737862E-4	3.707843095557273E-5	0.0014421837375766522
GOTERM_CC_ALL	GO:0044422~organelle part	10	71.43%	0.0368673468391256	S000003882, S000002706, S000003155, S000000195, S000005999, S000004997, S000003882, S000004028, S000004387, S000003159, 	14	2301	5632	1.7483081889861551	0.9999999999777655	0.5353835078549395	42.94864604210752
GOTERM_CC_ALL	GO:0033178~proton-transporting two-sector ATPase complex, catalytic domain	4	28.57%	6.414463893121058E-6	S000003882, S000002706, S000000195, S000003882, 	14	17	5632	94.65546218487394	0.0041798981622530595	1.994400309182076E-4	0.009582956878873006
GOTERM_CC_ALL	GO:0033177~proton-transporting two-sector ATPase complex, proton-transporting domain	3	21.43%	0.0010077286045780168	S000002706, S000005999, S000005999, 	14	21	5632	57.469387755102034	0.4823099464317113	0.024089493962627162	1.4950448954651918
GOTERM_CC_ALL	GO:0000276~mitochondrial proton-transporting ATP synthase complex, coupling factor F(o)	2	14.29%	0.027376315885587123	S000002706, S000005999, 	14	12	5632	67.04761904761905	0.9999999865729374	0.4427322586888206	33.94699076606338
GOTERM_CC_ALL	GO:0000275~mitochondrial proton-transporting ATP synthase complex, catalytic core F(1)	3	21.43%	7.340126705958842E-5	S000003882, S000000195, S000003882, 	14	6	5632	201.14285714285714	0.04680214738322663	0.001915474595515665	0.1096074222371568
GOTERM_CC_ALL	GO:0005743~mitochondrial inner membrane	10	71.43%	3.133119092481637E-11	S000003882, S000002706, S000003155, S000000195, S000005999, S000004997, S000003882, S000004028, S000004387, S000003159, 	14	191	5632	21.062079281974572	2.0459247185300455E-8	6.819749098774253E-9	4.680961174230447E-8
GOTERM_CC_ALL	GO:0000274~mitochondrial proton-transporting ATP synthase, stator stalk	2	14.29%	0.006909968533425321	S000002706, S000005999, 	14	3	5632	268.1904761904762	0.9891963501737456	0.14455501193220344	9.840977861323552
GOTERM_CC_ALL	GO:0005740~mitochondrial envelope	10	71.43%	3.1435985004983136E-9	S000003882, S000002706, S000003155, S000000195, S000005999, S000004997, S000003882, S000004028, S000004387, S000003159, 	14	319	5632	12.610837438423646	2.0527677120352195E-6	2.932527882748559E-7	4.6966224354072494E-6
GOTERM_CC_ALL	GO:0005739~mitochondrion	12	85.71%	1.328977450330144E-6	S000003882, S000002706, S000003155, S000000195, S000005999, S000004997, S000005999, S000003882, S000004028, S000004387, S000003439, S000003159, 	14	1154	5632	4.183213666749195	8.674464023651351E-4	4.821121845244303E-5	0.0019855104412713764
GOTERM_CC_ALL	GO:0045277~respiratory chain complex IV	5	35.71%	8.365377472985592E-9	S000003155, S000004997, S000004028, S000004387, S000003159, 	14	12	5632	167.61904761904765	5.462576611603431E-6	6.82823708353375E-7	1.2498103152402962E-5
GOTERM_CC_ALL	GO:0044455~mitochondrial membrane part	10	71.43%	3.5280572783016857E-13	S000003882, S000002706, S000003155, S000000195, S000005999, S000004997, S000003882, S000004028, S000004387, S000003159, 	14	117	5632	34.38339438339438	2.303972568284962E-10	2.303972568284962E-10	5.271338920920243E-10
GOTERM_CC_ALL	GO:0045267~proton-transporting ATP synthase, catalytic core	3	21.43%	1.4737764835078688E-5	S000003882, S000000195, S000003882, 	14	3	5632	402.2857142857143	0.009577670489531065	4.1833992163242684E-4	0.0220163639806481
GOTERM_CC_ALL	GO:0032991~macromolecular complex	13	92.86%	6.200301918298537E-6	S000004997, S000004387, S000003159, S000003882, S000002706, S000000195, S000003155, S000005999, S000000195, S000005999, S000003882, S000005999, S000004028, 	14	1725	5632	3.0317184265010355	0.0040406243253358065	2.0241999553805012E-4	0.00926302113514188
GOTERM_CC_ALL	GO:0019866~organelle inner membrane	10	71.43%	5.203286066955664E-11	S000003882, S000002706, S000003155, S000000195, S000005999, S000004997, S000003882, S000004028, S000004387, S000003159, 	14	202	5632	19.915134370579917	3.39774325341935E-8	8.494358216815101E-9	7.773847121583799E-8
GOTERM_CC_ALL	GO:0045265~proton-transporting ATP synthase, stator stalk	2	14.29%	0.006909968533425321	S000002706, S000005999, 	14	3	5632	268.1904761904762	0.9891963501737456	0.14455501193220344	9.840977861323552
GOTERM_CC_ALL	GO:0045263~proton-transporting ATP synthase complex, coupling factor F(o)	3	21.43%	4.406829632417675E-4	S000002706, S000005999, S000005999, 	14	14	5632	86.20408163265306	0.2501104878313618	0.011009310594931931	0.6563739649655287
GOTERM_CC_ALL	GO:0045261~proton-transporting ATP synthase complex, catalytic core F(1)	4	28.57%	8.008761082313701E-7	S000003882, S000002706, S000000195, S000003882, 	14	9	5632	178.79365079365078	5.228355818966968E-4	3.268523508093146E-5	0.0011965242358913386
GOTERM_CC_ALL	GO:0016020~membrane	13	92.86%	7.628592576013883E-6	S000004997, S000004387, S000003159, S000003882, S000002706, S000000195, S000003155, S000005999, S000000195, S000005999, S000003882, S000005999, S000004028, 	14	1756	5632	2.978197201431826	0.004969102909115897	2.26405727854595E-4	0.011396720953205097
GOTERM_CC_ALL	GO:0045259~proton-transporting ATP synthase complex	6	42.86%	1.4166066493008505E-9	S000003882, S000002706, S000000195, S000005999, S000005999, S000003882, 	14	25	5632	96.54857142857142	9.250436889818303E-7	1.541740075605702E-7	2.116449182576474E-6
GOTERM_CC_ALL	GO:0044446~intracellular organelle part	10	71.43%	0.0368673468391256	S000003882, S000002706, S000003155, S000000195, S000005999, S000004997, S000003882, S000004028, S000004387, S000003159, 	14	2301	5632	1.7483081889861551	0.9999999999777655	0.5353835078549395	42.94864604210752
"""

david_results_mf = """Category	Term	Count	%	PValue	Genes	List Total	Pop Hits	Pop Total	Fold Enrichment	Bonferroni	Benjamini	FDR
GOTERM_MF_ALL	GO:0046961~hydrogen ion transporting ATPase activity, rotational mechanism	7	50.00%	1.357188625187203E-10	S000003882, S000002706, S000000195, S000000195, S000005999, S000003882, S000005999, 	14	35	4927	70.38571428571429	2.4076526516925156E-7	2.1887753720584158E-8	2.3007645788553077E-7
GOTERM_MF_ALL	GO:0022804~active transmembrane transporter activity	7	50.00%	4.561468131602496E-6	S000003882, S000002706, S000000195, S000000195, S000005999, S000003882, S000005999, 	14	193	4927	12.764248704663212	0.00805941031507107	3.517669381594146E-4	0.0077325147965212615
GOTERM_MF_ALL	GO:0017111~nucleoside-triphosphatase activity	7	50.00%	1.354991458548405E-4	S000003882, S000002706, S000000195, S000000195, S000005999, S000003882, S000005999, 	14	349	4927	7.058739255014327	0.21368025699328053	0.009203226040080392	0.22945586557691078
GOTERM_MF_ALL	GO:0008553~hydrogen-exporting ATPase activity, phosphorylative mechanism	2	14.29%	0.015735007517678746	S000003882, S000003882, 	14	6	4927	117.30952380952381	0.9999999999993964	0.5849039042925119	23.575548401812018
GOTERM_MF_ALL	GO:0046933~hydrogen ion transporting ATP synthase activity, rotational mechanism	8	57.14%	1.504413377749123E-12	S000003882, S000002706, S000000195, S000005999, S000000195, S000005999, S000003882, S000005999, 	14	38	4927	74.09022556390977	2.668917753467781E-9	2.965464540594098E-10	2.550426536629402E-9
GOTERM_MF_ALL	GO:0015078~hydrogen ion transmembrane transporter activity	13	92.86%	8.312898389343022E-21	S000004997, S000004387, S000003159, S000003882, S000002706, S000000195, S000003155, S000005999, S000000195, S000005999, S000003882, S000005999, S000004028, 	14	90	4927	50.83412698412699	1.474708174269452E-17	1.474708174269452E-17	1.4092381372956447E-17
GOTERM_MF_ALL	GO:0015077~monovalent inorganic cation transmembrane transporter activity	13	92.86%	1.6571922570429097E-20	S000004997, S000004387, S000003159, S000003882, S000002706, S000000195, S000003155, S000005999, S000000195, S000005999, S000003882, S000005999, S000004028, 	14	95	4927	48.15864661654136	2.939859063994122E-17	1.469929531997061E-17	2.809343288076066E-17
GOTERM_MF_ALL	GO:0015075~ion transmembrane transporter activity	13	92.86%	1.3266048405395307E-16	S000004997, S000004387, S000003159, S000003882, S000002706, S000000195, S000003155, S000005999, S000000195, S000005999, S000003882, S000005999, S000004028, 	14	195	4927	23.461904761904762	1.9695356456850277E-13	3.941291737419306E-14	1.887379141862766E-13
GOTERM_MF_ALL	GO:0016887~ATPase activity	7	50.00%	2.851574368180932E-5	S000003882, S000002706, S000000195, S000000195, S000005999, S000003882, S000005999, 	14	265	4927	9.29622641509434	0.04932940179671719	0.002021460114576268	0.04833011644592711
GOTERM_MF_ALL	GO:0015405~P-P-bond-hydrolysis-driven transmembrane transporter activity	7	50.00%	9.769490154343295E-8	S000003882, S000002706, S000000195, S000000195, S000005999, S000003882, S000005999, 	14	101	4927	24.39108910891089	1.7329574628732747E-4	9.628329410094061E-6	1.6561645203028164E-4
GOTERM_MF_ALL	GO:0015399~primary active transmembrane transporter activity	7	50.00%	9.769490154343295E-8	S000003882, S000002706, S000000195, S000000195, S000005999, S000003882, S000005999, 	14	101	4927	24.39108910891089	1.7329574628732747E-4	9.628329410094061E-6	1.6561645203028164E-4
GOTERM_MF_ALL	GO:0015662~ATPase activity, coupled to transmembrane movement of ions, phosphorylative mechanism	2	14.29%	0.06406743892539128	S000003882, S000003882, 	14	25	4927	28.154285714285713	1.0	0.9684032470122852	67.45191745405069
GOTERM_MF_ALL	GO:0046872~metal ion binding	5	35.71%	0.07719554090708378	S000003882, S000002706, S000003155, S000000195, S000003882, 	14	640	4927	2.7494419642857144	1.0	0.9829564745750087	74.38322655397852
GOTERM_MF_ALL	GO:0043492~ATPase activity, coupled to movement of substances	7	50.00%	4.8652622253470385E-8	S000003882, S000002706, S000000195, S000000195, S000005999, S000003882, S000005999, 	14	90	4927	27.372222222222224	8.630602941672727E-5	5.753967045607489E-6	8.24779769370565E-5
GOTERM_MF_ALL	GO:0015002~heme-copper terminal oxidase activity	5	35.71%	7.691253005950271E-7	S000003155, S000004997, S000004028, S000004387, S000003159, 	14	30	4927	58.654761904761905	0.0013634983981221094	6.201756809931513E-5	0.0013038461507353105
GOTERM_MF_ALL	GO:0042626~ATPase activity, coupled to transmembrane movement of substances	7	50.00%	4.8652622253470385E-8	S000003882, S000002706, S000000195, S000000195, S000005999, S000003882, S000005999, 	14	90	4927	27.372222222222224	8.630602941672727E-5	5.753967045607489E-6	8.24779769370565E-5
GOTERM_MF_ALL	GO:0042625~ATPase activity, coupled to transmembrane movement of ions	7	50.00%	3.290094897579469E-9	S000003882, S000002706, S000000195, S000000195, S000005999, S000003882, S000005999, 	14	58	4927	42.47413793103448	5.836611263854152E-6	4.48971306687973E-7	5.577509576415451E-6
GOTERM_MF_ALL	GO:0042623~ATPase activity, coupled	7	50.00%	5.780183298730377E-6	S000003882, S000002706, S000000195, S000000195, S000005999, S000003882, S000005999, 	14	201	4927	12.256218905472638	0.010201681018396247	4.2716185735414136E-4	0.009798362529434002
GOTERM_MF_ALL	GO:0008324~cation transmembrane transporter activity	13	92.86%	1.244185803793163E-17	S000004997, S000004387, S000003159, S000003882, S000002706, S000000195, S000003155, S000005999, S000000195, S000005999, S000003882, S000005999, S000004028, 	14	161	4927	28.41659272404614	2.207185615929071E-14	5.517964039822678E-15	2.1091970603597518E-14
GOTERM_MF_ALL	GO:0005215~transporter activity	13	92.86%	9.331263693917314E-12	S000004997, S000004387, S000003159, S000003882, S000002706, S000000195, S000003155, S000005999, S000000195, S000005999, S000003882, S000005999, S000004028, 	14	488	4927	9.375146370023419	1.6553750037395787E-8	1.65537505925073E-9	1.581884623291785E-8
GOTERM_MF_ALL	GO:0019829~cation-transporting ATPase activity	7	50.00%	2.7146665610749877E-10	S000003882, S000002706, S000000195, S000000195, S000005999, S000003882, S000005999, 	14	39	4927	63.166666666666664	4.81581680311649E-7	4.0131815537414184E-8	4.60201854401987E-7
GOTERM_MF_ALL	GO:0043167~ion binding	5	35.71%	0.08465249594692495	S000003882, S000002706, S000003155, S000000195, S000003882, 	14	660	4927	2.666125541125541	1.0	0.9872049046718362	77.67510380858903
GOTERM_MF_ALL	GO:0016491~oxidoreductase activity	6	42.86%	0.0016156535426757536	S000003155, S000004997, S000004028, S000004387, S000003439, S000003159, 	14	361	4927	5.849228333992876	0.9432152372099303	0.08837982165926195	2.703911735463682
GOTERM_MF_ALL	GO:0016820~hydrolase activity, acting on acid anhydrides, catalyzing transmembrane movement of substances	7	50.00%	5.934326909367205E-8	S000003882, S000002706, S000000195, S000000195, S000005999, S000003882, S000005999, 	14	93	4927	26.489247311827956	1.0526942125099747E-4	6.579663508032851E-6	1.0060120366750525E-4
GOTERM_MF_ALL	GO:0016818~hydrolase activity, acting on acid anhydrides, in phosphorus-containing anhydrides	7	50.00%	1.8772210180800466E-4	S000003882, S000002706, S000000195, S000000195, S000005999, S000003882, S000005999, 	14	370	4927	6.658108108108109	0.28326583700053276	0.012259428518476279	0.3177584959434432
GOTERM_MF_ALL	GO:0016817~hydrolase activity, acting on acid anhydrides	7	50.00%	1.9634482734341306E-4	S000003882, S000002706, S000000195, S000000195, S000005999, S000003882, S000005999, 	14	373	4927	6.604557640750671	0.2941481609246992	0.011940209452176997	0.3323313942078632
GOTERM_MF_ALL	GO:0003824~catalytic activity	13	92.86%	0.0012913234405410655	S000004997, S000004387, S000003159, S000003439, S000003882, S000002706, S000000195, S000003155, S000000195, S000005999, S000003882, S000005999, S000004028, 	14	2405	4927	1.9023166023166025	0.8989649855976286	0.0735633440992598	2.1667037480417095
GOTERM_MF_ALL	GO:0016462~pyrophosphatase activity	7	50.00%	1.8772210180800466E-4	S000003882, S000002706, S000000195, S000000195, S000005999, S000003882, S000005999, 	14	370	4927	6.658108108108109	0.28326583700053276	0.012259428518476279	0.3177584959434432
GOTERM_MF_ALL	GO:0016676~oxidoreductase activity, acting on heme group of donors, oxygen as acceptor	5	35.71%	7.691253005950271E-7	S000003155, S000004997, S000004028, S000004387, S000003159, 	14	30	4927	58.654761904761905	0.0013634983981221094	6.201756809931513E-5	0.0013038461507353105
GOTERM_MF_ALL	GO:0016675~oxidoreductase activity, acting on heme group of donors	5	35.71%	7.691253005950271E-7	S000003155, S000004997, S000004028, S000004387, S000003159, 	14	30	4927	58.654761904761905	0.0013634983981221094	6.201756809931513E-5	0.0013038461507353105
GOTERM_MF_ALL	GO:0022892~substrate-specific transporter activity	13	92.86%	1.045535361873502E-12	S000004997, S000004387, S000003159, S000003882, S000002706, S000000195, S000003155, S000005999, S000000195, S000005999, S000003882, S000005999, S000004028, 	14	407	4927	11.24096174096174	1.8547117175415906E-9	2.3183899244827444E-10	1.7723711387418462E-9
GOTERM_MF_ALL	GO:0022891~substrate-specific transmembrane transporter activity	13	92.86%	1.1436221376671628E-13	S000004997, S000004387, S000003159, S000003882, S000002706, S000000195, S000003155, S000005999, S000000195, S000005999, S000003882, S000005999, S000004028, 	14	339	4927	13.495785924989466	2.0286217150555785E-10	3.381039892502713E-11	1.9385604232979858E-10
GOTERM_MF_ALL	GO:0022890~inorganic cation transmembrane transporter activity	13	92.86%	2.6125070468606044E-18	S000004997, S000004387, S000003159, S000003882, S000002706, S000000195, S000003155, S000005999, S000000195, S000005999, S000003882, S000005999, S000004028, 	14	142	4927	32.21881287726358	4.634587501130712E-15	1.544862500376904E-15	4.428833833827902E-15
GOTERM_MF_ALL	GO:0004129~cytochrome-c oxidase activity	5	35.71%	7.691253005950271E-7	S000003155, S000004997, S000004028, S000004387, S000003159, 	14	30	4927	58.654761904761905	0.0013634983981221094	6.201756809931513E-5	0.0013038461507353105
GOTERM_MF_ALL	GO:0016787~hydrolase activity	7	50.00%	0.030218055645008027	S000003882, S000002706, S000000195, S000000195, S000005999, S000003882, S000005999, 	14	988	4927	2.493421052631579	1.0	0.8078538878815004	40.55798333297395
GOTERM_MF_ALL	GO:0022857~transmembrane transporter activity	13	92.86%	6.05182729099852E-13	S000004997, S000004387, S000003159, S000003882, S000002706, S000000195, S000003155, S000005999, S000000195, S000005999, S000003882, S000005999, S000004028, 	14	389	4927	11.761109070877708	1.0735938804629086E-9	1.5337053849151516E-10	1.0259348925956147E-9
"""

def proces_david(dav):
    lines = [line.split("\t") for line in dav.split("\n") if line]
    keys = lines[0]
    return dict([(line[1].split("~")[0], dict(zip(keys, line))) for line in lines])

terms = [["GO:0009058", "GO:0006119"], ["GO:0031967", "GO:0044455"], ["GO:0046933", "GO:0003824"]]
print "\n".join(cluster_genes)

for aspect, terms, david in zip(["P", "C", "F"], terms, [proces_david(david_results_bp), proces_david(david_results_cc), proces_david(david_results_mf)]):
    enriched_terms = annotations.GetEnrichedTerms(cluster_genes, reference_genes, aspect=aspect, prob=obiProb.Hypergeometric())
#    print enriched_terms
    for term in terms:
        print "Term: %s - %s" % (term, ontology[term].name)
        print "    Annotated genes in reference: %i from %i" % (enriched_terms[term][2], len(reference_genes))
        print "    Annotated genes in cluster: %i from %i" % (len(enriched_terms[term][0]), len(cluster_genes))
        print "    Enrichment: %.3f" % ((len(enriched_terms[term][0]) / len(cluster_genes)) / (enriched_terms[term][2]/len(reference_genes)))
        print "    p-value: %f" % (enriched_terms[term][1])
        print "    Comment: results from NCBI David (%s):" % david_date
        print "    Annotated genes in reference: %s from %s" % (david[term]["Pop Hits"], david[term]["Pop Total"])
        print "    Annotated genes in cluster: %s from %s" % (david[term]["Count"], david[term]["List Total"])
        print "    Enrichment: %s" % david[term]["Fold Enrichment"]
        print "    p-value: %s" % david[term]["PValue"]
    

