import os
from time import time

from hommod_rest.factory import create_app, create_celery_app
from hommod_rest.services.modelutils import TemplateID

import hommod_rest.default_settings as settings

import logging
_log = logging.getLogger(__name__)


class TestTasks:

    @classmethod
    def setup_class(self):
        self.app = create_app({'TESTING': True, 'CELERY_ALWAYS_EAGER': True})
        self.celery = create_celery_app(self.app)

    def test_remodel_oldest_hg(self):
        from hommod_rest.tasks import remodel_oldest_hg

        model_paths = []
        while len(model_paths) <= 0:
            model_paths = remodel_oldest_hg()

        for path in model_paths:

            # Verify that the model was placed in the model dir.
            assert (os.path.dirname(path).strip('/') == settings.HGMODELDIR.strip('/'))

            # Verify that the model has been created less than an hour ago.
            assert ((time() - os.path.getmtime(path)) < 3600)


    def test_create_model(self):
        # Best pick a simple model which doesn't take much time ..
        from hommod_rest.tasks import create_model
        path = create_model("IICCASITARSDFDVCRLAGTAQAVCAVFVGCVIVPAATCPGDFGD",
                            "CRAAB", 25, None)

        _log.debug("Recieved model path: \'%s\'" % path)

        assert (len(path) > 0)

    def test_create_model_4RH7_A(self):
        # This is a slow model!
        from hommod_rest.tasks import create_model
        path = create_model(
            "MANGTADVRKLFIFTTTQNYFGLMSELWDQPLLCNCLEINNFLDDGNQMLLRVQRSDAGISFSNTIEFGDTK" +
            "DKVLVFFKLRPEVITDENLHDNILVSSMLESPISSLYQAVRQVFAPMLLKDQEWSRNFDPKLQNLLSELEAG" +
            "LGIVLRRSDTNLTKLKFKEDDTRGILTPSDEFQFWIEQAHRGNKQISKERANYFKELFETIAREFYNLDSLS" +
            "LLEVVDLVETTQDVVDDVWRQTEHDHYPESRMLHLLDIIGGSFGRFVQKKLGTLNLWEDPYYLVKESLKAGI" +
            "SICEQWVIVCNHLTGQVWQRYVPHPWKNEKYFPETLDKLGKRLEEVLAIRTIHEKFLYFLPASEEKIICLTR" +
            "VFEPFTGLNPVQYNPYTEPLWKAAVSQYEKIIAPAEQKIAGKLKNYISEIQDSPQQLLQAFLKYKELVKRPT" +
            "ISKELMLERETLLARLVDSIKDFRLDFENRCRGIPGDASGPLSGKNLSEVVNSIVWVRQLELKVDDTIKIAE" +
            "ALLSDLPGFRCFHQSAKDLLDQLKLYEQEQFDDWSRDIQSGLSDSRSGLCIEASSRIMELDSNDGLLKVHYS" +
            "DRLVILLREVRQLSALGFVIPAKIQQVANIAQKFCKQAIILKQVAHFYNSIDQQMIQSQRPMMLQSALAFEQ" +
            "IIKNSKAGSGGKSQITWDNPKELEGYIQKLQNAAERLATENRKLRKWHTTFCEKVVVLMNIDLLRQQQRWKD" +
            "GLQELRTGLATVEAQGFQASDMHAWKQHWNHQLYKALEHQYQMGLEALNENLPEINIDLTYKQGRLQFRPPF" +
            "EEIRAKYYREMKRFIGIPNQFKGVGEAGDESIFSIMIDRNASGFLTIFSKAEDLFRRLSAVLHQHKEWIVIG" +
            "QVDMEALVEKHLFTVHDWEKNFKALKIKGKEVERLPSAVKVDCLNINCNPVKTVIDDLIQKLFDLLVLSLKK" +
            "SIQAHLHEIDTFVTEAMEVLTIMPQSVEEIGDANLQYSKLQERKPEILPLFQEAEDKNRLLRTVAGGGLETI" +
            "SNLKAKWDKFELMMESHQLMIKDQIEVMKGNVKSRLQIYYQELEKFKARWDQLKPGDDVIETGQHNTLDKSA" +
            "KLIKEKKIEFDDLEVTRKKLVDDCHHFRLEEPNFSLASSISKDIESCAQIWAFYEEFQQGFQEMANEDWITF" +
            "RTKTYLFEEFLMNWHDRLRKVEEHSVMTVKLQSEVDKYKIVIPILKYVRGEHLSPDHWLDLFRLLGLPRGTS" +
            "LEKLLFGDLLRVADTIVAKAADLKDLNSRAQGEVTIREALRELDLWGVGAVFTLIDYEDSQSRTMKLIKDWK" +
            "DIVNQVGDNRCLLQSLKDSPYYKGFEDKVSIWERKLAELDEYLQNLNHIQRKWVYLEPIFGRGALPKEQTRF" +
            "NRVDEDFRSIMTDIKKDNRVTTLTTHAGIRNSLLTILDQLQRCQKSLNEFLEEKRSAFPRFYFIGDDDLLEI" +
            "LGQSTNPSVIQSHLKKLFAGINSVCFDEKSKHITAMKSLEGEVVPFKNKVPLSNNVETWLNDLALEMKKTLE" +
            "QLLKECVTTGRSSQGAVDPSLFPSQILCLAEQIKFTEDVENAIKDHSLHQIETQLVNKLEQYTNIDTSSEDP" +
            "GNTESGILELKLKALILDIIHNIDVVKQLNQIQVHTTEDWAWKKQLRFYMKSDHTCCVQMVDSEFQYTYEYQ" +
            "GNASKLVYTPLTDKCYLTLTQAMKMGLGGNPYGPAGTGKTESVKALGGLLGRQVLVFNCDEGIDVKSMGRIF" +
            "VGLVKCGAWGCFDEFNRLEESVLSAVSMQIQTIQDALKNHRTVCELLGKEVEVNSNSGIFITMNPAGKGYGG" +
            "RQKLPDNLKQLFRPVAMSHPDNELIAEVILYSEGFKDAKVLSRKLVAIFNLSRELLTPQQHYDWGLRALKTV" +
            "LRGSGNLLRQLNKSGTTQNANESHIVVQALRLNTMSKFTFTDCTRFDALIKDVFPGIELKEVEYDELSAALK" +
            "QVFEEANYEIIPNQIKKALELYEQLCQRMGVVIVGPSGAGKSTLWRMLRAALCKTGKVVKQYTMNPKAMPRY" +
            "QLLGHIDMDTREWSDGVLTNSARQVVREPQDVSSWIICDGDIDPEWIESLNSVLDDNRLLTMPSGERIQFGP" +
            "NVNFVFETHDLSCASPATISRMGMIFLSDEETDLNSLIKSWLRNQPAEYRNNLENWIGDYFEKALQWVLKQN" +
            "DYVVETSLVGTVMNGLSHLHGCRDHDEFIINLIRGLGGNLNMKSRLEFTKEVFHWARESPPDFHKPMDTYYD" +
            "STRGRLATYVLKKPEDLTADDFSNGLTLPVIQTPDMQRGLDYFKPWLSSDTKQPFILVGPEGCGKGMLLRYA" +
            "FSQLRSTQIATVHCSAQTTSRHLLQKLSQTCMVISTNTGRVYRPKDCERLVLYLKDINLPKLDKWGTSTLVA" +
            "FLQQVLTYQGFYDENLEWVGLENIQIVASMSAGGRLGRHKLTTRFTSIVRLCSIDYPEREQLQTIYGAYLEP" +
            "VLHKNLKNHSIWGSSSKIYLLAGSMVQVYEQVRAKFTVDDYSHYFFTPCILTQWVLGLFRYDLEGGSSNHPL" +
            "DYVLEIVAYEARRLFRDKIVGAKELHLFDIILTSVFQGDWGSDILDNMSDSFYVTWGARHNSGARAAPGQPL" +
            "PPHGKPLGKLNSTDLKDVIKKGLIHYGRDNQNLDILLFHEVLEYMSRIDRVLSFPGGSLLLAGRSGVGRRTI" +
            "TSLVSHMHGAVLFSPKISRGYELKQFKNDLKHVLQLAGIEAQQVVLLLEDYQFVHPTFLEMINSLLSSGEVP" +
            "GLYTLEELEPLLLPLKDQASQDGFFGPVFNYFTYRIQQNLHIVLIMDSANSNFMINCESNPALHKKCQVLWM" +
            "EGWSNSSMKKIPEMLFSETGGGEKYNDKKRKEEKKKNSVDPDFLKSFLLIHESCKAYGATPSRYMTFLHVYS" +
            "AISSSKKKELLKRQSHLQAGVSKLNEAKALVDELNRKAGEQSVLLKTKQDEADAALQMITVSMQDASEQKTE" +
            "LERLKHRIAEEVVKIEERKNKIDDELKEVQPLVNEAKLAVGNIKPESLSEIRSLRMPPDVIRDILEGVLRLM" +
            "GIFDTSWVSMKSFLAKRGVREDIATFDARNISKEIRESVEELLFKNKGSFDPKNAKRASTAAAPLAAWVKAN" +
            "IQYSHVLERIHPLETEQAGLESNLKKTEDRKRKLEELLNSVGQKVSELKEKFQSRTSEAAKLEAEVSKAQET" +
            "IKAAEVLINQLDREHKRWNAQVVEITEELATLPKRAQLAAAFITYLSAAPESLRKTCLEEWTKSAGLEKFDL" +
            "RRFLCTESEQLIWKSEGLPSDDLSIENALVILQSRVCPFLIDPSSQATEWLKTHLKDSRLEVINQQDSNFIT" +
            "ALELAVRFGKTLIIQEMDGVEPVLYPLLRRDLVAQGPRYVVQIGDKIIDYNEEFRLFLSTRNPNPFIPPDAA" +
            "SIVTEVNFTTTRSGLRGQLLALTIQHEKPDLEEQKTKLLQQEEDKKIQLAKLEESLLETLATSQGNILENKD" +
            "LIESLNQTKASSALIQESLKESYKLQISLDQERDAYLPLAESASKMYFIISDLSKINNMYRFSLAAFLRLFQ" +
            "RALQNKQDSENTEQRIQSLISSLQHMVYEYICRCLFKADQLMFALHFVRGMHPELFQENEWDTFTGVVVGDM" +
            "LRKADSQQKIRDQLPSWIDQERSWAVATLKIALPSLYQTLCFEDAALWRTYYNNSMCEQEFPSILAKKVSLF" +
            "QQILVVQALRPDRLQSAMALFACKTLGLKEVSPLPLNLKRLYKETLEIEPILIIISPGADPSQELQELANAE" +
            "RSGECYHQVAMGQGQADLAIQMLKECARNGDWLCLKNLHLVVSWLPVLEKELNTLQPKDTFRLWLTAEVHPN" +
            "FTPILLQSSLKITYESPPGLKKNLMRTYESWTPEQISKKDNTHRAHALFSLAWFHAACQERRNYIPQGWTKF" +
            "YEFSLSDLRAGYNIIDRLFDGAKDVQWEFVHGLLENAIYGGRIDNYFDLRVLQSYLKQFFNSSVIDVFNQRN" +
            "KKSIFPYSVSLPQSCSILDYRAVIEKIPEDDKPSFFGLPANIARSSQRMISSQVISQLRILGRSITAGSKFD" +
            "REIWSNELSPVLNLWKKLNQNSNLIHQKVPPPNDRQGSPILSFIILEQFNAIRLVQSVHQSLAALSKVIRGT" +
            "TLLSSEVQKLASALLNQKCPLAWQSKWEGPEDPLQYLRGLVARALAIQNWVDKAEKQALLSETLDLSELFHP" +
            "DTFLNALRQETARAVGRSVDSLKFVASWKGRLQEAKLQIKISGLLLEGCSFDGNQLSENQLDSPSVSSVLPC" +
            "FMGWIPQDACGPYSPDECISLPVYTSAERDRVVTNIDVPCGGNQDQWIQCGAALFLKNQ",
            "HUMAN", 3373, TemplateID('4RH7', 'A'))

        assert (len(path) > 0)

    def test_take_template(self):
        # Best pick a simple model which doesn't take much time ..
        from hommod_rest.tasks import create_model
        path = create_model("TTCCPSIVARSNFNVCRLPGTPEAICATYTGCIIIPGATCPGDYAN",
                            "CRAAB", 25, None)

        _log.debug("Recieved model path: \'%s\'" % path)

        assert (len(path) > 0)

    def test_model_1R6F_A(self):
        from hommod_rest.tasks import create_model
        path = create_model(
                "MERAESSSTEPAKAIKPIDRKSVHQICSGQVVLSLSTAVKELVENSLDAGATNIDLKL" +
                "KDYGVDLIEVSDNGCGVEEENFEGLTLKHHTSKIQEFADLTQVETFGFRGEALSSLCA" +
                "LSDVTISTCHASAKVGTRLMFDHNGKIIQKTPYPRPRGTTVSVQQLFSTLPVRHKEFQ" +
                "RNIKKEYAKMVQVLHAYCIISAGIRVSCTNQLGQGKRQPVVCTGGSPSIKENIGSVFG" +
                "QKQLQSLIPFVQLPPSDSVCEEYGLSCSDALHNLFYISGFISQCTHGVGRSSTDRQFF" +
                "FINRRPCDPAKVCRLVNEVYHMYNRHQYPFVVLNISVDSECVDINVTPDKRQILLQEE" +
                "KLLLAVLKTSLIGMFDSDVNKLNVSQQPLLDVEGNLIKMHAADLEKPMVEKQDQSPSL" +
                "RTGEEKKDVSISRLREAFSLRHTTENKPHSPKTPEPRRSPLGQKRGMLSSSTSGAISD" +
                "KGVLRPQKEAVSSSHGPSDPTDRAEVEKDSGHGSTSVDSEGFSIPDTGSHCSSEYAAS" +
                "SPGDRGSQEHVDSQEKAPETDDSFSDVDCHSNQEDTGCKFRVLPQPTNLATPNTKRFK" +
                "KEEILSSSDICQKLVNTQDMSASQVDVAVKINKKVVPLDFSMSSLAKRIKQLHHEAQQ" +
                "SEGEQNYRKFRAKICPGENQAAEDELRKEISKTMFAEMEIIGQFNLGFIITKLNEDIF" +
                "IVDQHATDEKYNFEMLQQHTVLQGQRLIAPQTLNLTAVNEAVLIENLEIFRKNGFDFV" +
                "IDENAPVTERAKLISLPTSKNWTFGPQDVDELIFMLSDSPGVMCRPSRVKQMFASRAC" +
                "RKSVMIGTALNTSEMKKLITHMGEMDHPWNCPHGRPTMRHIANLGVISQN",
                "HUMAN", 470, TemplateID("1R6F", 'A'))

    def test_model_3UX9_A(self):
        from hommod_rest.tasks import create_model
        path = create_model(
            "MASPFALLMVLVVLSCKSSCSLGCDLPETHSLDNRRTLMLLAQMSRISPSSCLMDRHDFGFP" +
            "QEEFDGNQFQKAPAISVLHELIQQIFNLFTTKDSSAAWDEDLLDKFCTELYQQLNDLEACVM" +
            "QEERVGETPLMNADSILAVKKYFRRITLYLTEKKYSPCAWEVVRAEIMRSLSLSTNLQERLR" +
            "RKE", "HUMAN", 100, TemplateID("3UX9", 'A'))

        assert (len(path) > 0)

    def test_model_3JBH_A(self):
        from hommod_rest.tasks import create_model
        path = create_model(
            "MGDSEMAVFGAAAPYLRKSEKERLEAQTRPFDLKKDVFVPDDKQEFVKAKIVSREGGKVTAE" +
            "TEYGKTVTVKEDQVMQQNPPKFDKIEDMAMLTFLHEPAVLYNLKDRYGSWMIYTYSGLFCVT" +
            "VNPYKWLPVYTPEVVAAYRGKKRSEAPPHIFSISDNAYQYMLTDRENQSILITGESGAGKTV" +
            "NTKRVIQYFAVIAAIGDRSKKDQSPGKGTLEDQIIQANPALEAFGNAKTVRNDNSSRFGKFI" +
            "RIHFGATGKLASADIETYLLEKSRVIFQLKAERDYHIFYQILSNKKPELLDMLLITNNPYDY" +
            "AFISQGETTVASIDDAEELMATDNAFDVLGFTSEEKNSMYKLTGAIMHFGNMKFKLKQREEQ" +
            "AEPDGTEEADKSAYLMGLNSADLLKGLCHPRVKVGNEYVTKGQNVQQVIYATGALAKAVYER" +
            "MFNWMVTRINATLETKQPRQYFIGVLDIAGFEIFDFNSFEQLCINFTNEKLQQFFNHHMFVL" +
            "EQEEYKKEGIEWTFIDFGMDLQACIDLIEKPMGIMSILEEECMFPKATDMTFKAKLFDNHLG" +
            "KSANFQKPRNIKGKPEAHFSLIHYAGIVDYNIIGWLQKNKDPLNETVVGLYQKSSLKLLSTL" +
            "FANYAGADAPIEKGKGKAKKGSSFQTVSALHRENLNKLMTNLRSTHPHFVRCIIPNETKSPG" +
            "VMDNPLVMHQLRCNGVLEGIRICRKGFPNRILYGDFRQRYRILNPAAIPEGQFIDSRKGAEK" +
            "LLSSLDIDHNQYKFGHTKVFFKAGLLGLLEEMRDERLSRIITRIQAQSRGVLARMEYKKLLE" +
            "RRDSLLVIQWNIRAFMGVKNWPWMKLYFKIKPLLKSAEREKEMASMKEEFTRLKEALEKSEA" +
            "RRKELEEKMVSLLQEKNDLQLQVQAEQDNLADAEERCDQLIKNKIQLEAKVKEMNERLEDEE" +
            "EMNAELTAKKRKLEDECSELKRDIDDLELTLAKVEKEKHATENKVKNLTEEMAGLDEIIAKL" +
            "TKEKKALQEAHQQALDDLQAEEDKVNTLTKAKVKLEQQVDDLEGSLEQEKKVRMDLERAKRK" +
            "LEGDLKLTQESIMDLENDKQQLDERLKKKDFELNALNARIEDEQALGSQLQKKLKELQARIE" +
            "ELEEELEAERTARAKVEKLRSDLSRELEEISERLEEAGGATSVQIEMNKKREAEFQKMRRDL" +
            "EEATLQHEATAAALRKKHADSVAELGEQIDNLQRVKQKLEKEKSEFKLELDDVTSNMEQIIK" +
            "AKANLEKMCRTLEDQMNEHRSKAEETQRSVNDLTSQRAKLQTENGELSRQLDEKEALISQLT" +
            "RGKLTYTQQLEDLKRQLEEEVKAKNALAHALQSARHDCDLLREQYEEETEAKAELQRVLSKA" +
            "NSEVAQWRTKYETDAIQRTEELEEAKKKLAQRLQEAEEAVEAVNAKCSSLEKTKHRLQNEIE" +
            "DLMVDVERSNAAAAALDKKQRNFDKILAEWKQKYEESQSELESSQKEARSLSTELFKLKNAY" +
            "EESLEHLETFKRENKNLQEEISDLTEQLGSSGKTIHELEKVRKQLEAEKMELQSALEEAEAS" +
            "LEHEEGKILRAQLEFNQIKAEIERKLAEKDEEMEQAKRNHLRVVDSLQTSLDAETRSRNEAL" +
            "RVKKKMEGDLNEMEIQLSHANRMAAEAQKQVKSLQSLLKDTQIQLDDAVRANDDLKENIAIV" +
            "ERRNNLLQAELEELRAVVEQTERSRKLAEQELIETSERVQLLHSQNTSLINQKKKMDADLSQ" +
            "LQTEVEEAVQECRNAEEKAKKAITDAAMMAEELKKEQDTSAHLERMKKNMEQTIKDLQHRLD" +
            "EAEQIALKGGKKQLQKLEARVRELENELEAEQKRNAESVKGMRKSERRIKELTYQTEEDRKN" +
            "LLRLQDLVDKLQLKVKAYKRQAEEAEEQANTNLSKFRKVQHELDEAEERADIAESQVNKLRA" +
            "KSRDIGTKGLNEE", "HUMAN", 500, TemplateID("3JBH", 'A'))

    def test_model_4CKG_A(self):
        from hommod_rest.tasks import create_model
        path = create_model(
            "MGHPPLEFSDCYLDSPDFRERLKCYEQELERTNKFIKDVIKDGNALISAMRNYSSAVQKFSQ" +
            "TLQSFQFDFIGDTLTDDEINIAESFKEFAELLNEVENERMMMVHNASDLLIKPLENFRKEQI" +
            "GFTKERKKKFEKDGERFYSLLDRHLHLSSKKKESQLQEADLQVDKERHNFFESSLDYVYQIQ" +
            "EVQESKKFNIVEPVLAFLHSLFISNSLTVELTQDFLPYKQQLQLSLQNTRNHFSSTREEMEE" +
            "LKKRMKEAPQTCKLPGQPTIEGYLYTQEKWALGISWVKYYCQYEKETKTLTMTPMEQKPGAK" +
            "QGPLDLTLKYCVRRKTESIDKRFCFDIETNERPGTITLQALSEANRRLWMEAMDGKEPIYHS" +
            "PITKQQEMELNEVGFKFVRKCINIIETKGIKTEGLYRTVGSNIQVQKLLNAFFDPKCPGDVD" +
            "FHNSDWDIKTITSSLKFYLRNLSEPVMTYRLHKELVSAAKSDNLDYRLGAIHSLVYKLPEKN" +
            "REMLELLIRHLVNVCEHSKENLMTPSNMGVIFGPTLMRAQEDTVAAMMNIKFQNIVVEILIE" +
            "HFGKIYLGPPEESAAPPVPPPRVTARRHKPITISKRLLRERTVFYTSSLDESEDEIQHQTPN" +
            "GTITSSIEPPKPPQHPKLPIQRSGETDPGRKSPSRPILDGKLEPCPEVDVGKLVSRLQDGGT" +
            "KITPKATNGPMPGSGPTKTPSFHIKRPAPRPLAHHKEGDADSFSKVRPPGEKPTIIRPPVRP" +
            "PDPPCRAATPQKPEPKPDIVAGNAGEITSSVVASRTRFFETASRKTGSSQGRLPGDES",
            "HUMAN", 100, TemplateID("4CKG", 'A'))

    def test_model_3WTS_A(self):
        from hommod_rest.tasks import create_model
        path = create_model(
            "MRIPVDASTSRRFTPPSTALSPGKMSEALPLGAPDAGAALAGKLRSGDRSMVEVLADHPGEL" +
            "VRTDSPNFLCSVLPTHWRCNKTLPIAFKVVALGDVPDGTLVTVMAGNDENYSAELRNATAAM" +
            "KNQVARFNDLRFVGRSGRGKSFTLTITVFTNPPQVATYHRAIKITVDGPREPRRHRQKLDDQ" +
            "TKPGSLSFSERLSELEQLRRTAMRVSPHHPAPTPNPRASLNHSTAFNPQPQSQMQDTRQIQP" +
            "SPPWSYDQSYQYLGSIASPSVHPATPISPGRASGMTTLSAELSSRLSTAPDLTAFSDPRQFP" +
            "ALPSISDPRMHYPGAFTYSPTPVTSGIGIGMSAMGSATRYHTYLPPPYPGSSQAQGGPFQAS" +
            "SPSYHLYYGASAGSYQFSMVGGERSPPRILPPCTNASTGSALLNPSLPNQSDVVEAEGSHSN" +
            "SPTNMAPSARLEEAVWRPY", "HUMAN", 100, TemplateID("3WTS", 'A'))

    def test_model_4WFB(self):
        from hommod_rest.tasks import create_model
        path = create_model(
"MFSFVDLRLLLLLAATALLTHGQEEGQVEGQDEDIPPITCVQNGLRYHDRDVWKPEPCRICVCDNGKVLCDDVI" +
"CDETKNCPGAEVPEGECCPVCPDGSESPTDQETTGVEGPKGDTGPRGPRGPAGPPGRDGIPGQPGLPGPPGPPG" +
"PPGPPGLGGNFAPQLSYGYDEKSTGGISVPGPMGPSGPRGLPGPPGAPGPQGFQGPPGEPGEPGASGPMGPRGP" +
"PGPPGKNGDDGEAGKPGRPGERGPPGPQGARGLPGTAGLPGMKGHRGFSGLDGAKGDAGPAGPKGEPGSPGENG" +
"APGQMGPRGLPGERGRPGAPGPAGARGNDGATGAAGPPGPTGPAGPPGFPGAVGAKGEAGPQGPRGSEGPQGVR" +
"GEPGPPGPAGAAGPAGNPGADGQPGAKGANGAPGIAGAPGFPGARGPSGPQGPGGPPGPKGNSGEPGAPGSKGD" +
"TGAKGEPGPVGVQGPPGPAGEEGKRGARGEPGPTGLPGPPGERGGPGSRGFPGADGVAGPKGPAGERGSPGPAG" +
"PKGSPGEAGRPGEAGLPGAKGLTGSPGSPGPDGKTGPPGPAGQDGRPGPPGPPGARGQAGVMGFPGPKGAAGEP" +
"GKAGERGVPGPPGAVGPAGKDGEAGAQGPPGPAGPAGERGEQGPAGSPGFQGLPGPAGPPGEAGKPGEQGVPGD" +
"LGAPGPSGARGERGFPGERGVQGPPGPAGPRGANGAPGNDGAKGDAGAPGAPGSQGAPGLQGMPGERGAAGLPG" +
"PKGDRGDAGPKGADGSPGKDGVRGLTGPIGPPGPAGAPGDKGESGPSGPAGPTGARGAPGDRGEPGPPGPAGFA" +
"GPPGADGQPGAKGEPGDAGAKGDAGPPGPAGPAGPPGPIGNVGAPGAKGARGSAGPPGATGFPGAAGRVGPPGP" +
"SGNAGPPGPPGPAGKEGGKGPRGETGPAGRPGEVGPPGPPGPAGEKGSPGADGPAGAPGTPGPQGIAGQRGVVG" +
"LPGQRGERGFPGLPGPSGEPGKQGPSGASGERGPPGPMGPPGLAGPPGESGREGAPGAEGSPGRDGSPGAKGDR" +
"GETGPAGPPGAPGAPGAPGPVGPAGKSGDRGETGPAGPTGPVGPVGARGPAGPQGPRGDKGETGEQGDRGIKGH" +
"RGFSGLQGPPGPPGSPGEQGPSGASGPAGPRGPPGSAGAPGKDGLNGLPGPIGPPGPRGRTGDAGPVGPPGPPG" +
"PPGPPGPPSAGFDFSFLPQPPQEKAHDGGRYYRADDANVVRDRDLEVDTTLKSLSQQIENIRSPEGSRKNPART" +
"CRDLKMCHSDWKSGEYWIDPNQGCNLDAIKVFCNMETGETCVYPTQPSVAQKNWYISKNPKDKRHVWFGESMTD" +
"GFQFEYGGQGSDPADVAIQLTFLRLMSTEASQNITYHCKNSVAYMDQQTGNLKKALLLQGSNEIEIRAEGNSRF" +
"TYSVTVDGCTSHTGAWGKTVIEYKTTKTSRLPIIDVAPLDVGAPDQEFGFDVGPVCFL",
            "HUMAN", 621, TemplateID("4WFB", 'X'))

    def test_ANGL3_HUMAN(self):
        from hommod_rest.tasks import create_model
        path = create_model(
"MFTIKLLLFIVPLVISSRIDQDNSSFDSLSPEPKSRFAMLDDVKILANGLLQLGHGLKDFVHKTKGQINDIF" +
"QKLNIFDQSFYDLSLQTSEIKEEEKELRRTTYKLQVKNEEVKNMSLELNSKLESLLEEKILLQQKVKYLEEQ" +
"LTNLIQNQPETPEHPEVTSLKTFVEKQDNSIKDLLQTVEDQYKQLNQQHSQIKEIENQLRRTSIQEPTEISL" +
"SSKPRAPRTTPFLQLNEIRNVKHDGIPAECTTIYNRGEHTSGMYAIRPSNSQVFHVYCDVISGSPWTLIQHR" +
"IDGSQNFNETWENYKYGFGRLDGEFWLGLEKIYSIVKQSNYVLRIELEDWKDNKHYIEYSFYLGNHETNYTL" +
"HLVAITGNVPNAIPENKDLVFSTWDHKAKGHFNCPEGYSGGWWWHDECGENNLNGKYNKPRAKSKPERRRGL" +
"SWKSQNGRLYSIKSTKMLIHPTDSESFE",
            "HUMAN", 360, None)
        assert(len(path) > 0)

    def test_blood_clotting(self):
        from hommod_rest.tasks import create_model
        path = create_model(
"MGNKQTIFTEEQLDNYQDCTFFNKKDILKLHARFYELAPNLVPMDYRKSPIVHVPMSLIIQMPELRENPFKE" +
"RIVEAFSEDGEGNLTFNDFVDMFSVLCESAPRELKANYAFKIYDFNTDNFICKEDLEMTLARLTKSELEEDE" +
"VVLVCDKVIEEADLDGDGKLGFADFEDMIAKAPDFLSTFHIRI", "HUMAN", 52, TemplateID("1DGU", 'A'))
        assert(len(path) > 0)

    def test_LYAG_HUMAN(self):
        from hommod_rest.tasks import create_model
        try:
            path = create_model(
"MGVRHPPCSHRLLAVCALVSLATAALLGHILLHDFLLVPRELSGSSPVLEETHPAHQQGASRPGPRDAQAHP" +
"GRPRAVPTQCDVPPNSRFDCAPDKAITQEQCEARGCCYIPAKQGLQGAQMGQPWCFFPPSYPSYKLENLSSS" +
"EMGYTATLTRTTPTFFPKDILTLRLDVMMETENRLHFTIKDPANRRYEVPLETPHVHSRAPSPLYSVEFSEE" +
"PFGVIVRRQLDGRVLLNTTVAPLFFADQFLQLSTSLPSQYITGLAEHLSPLMLSTSWTRITLWNRDLAPTPG" +
"ANLYGSHPFYLALEDGGSAHGVFLLNSNAMDVVLQPSPALSWRSTGGILDVYIFLGPEPKSVVQQYLDVVGY" +
"PFMPPYWGLGFHLCRWGYSSTAITRQVVENMTRAHFPLDVQWNDLDYMDSRRDFTFNKDGFRDFPAMVQELH" +
"QGGRRYMMIVDPAISSSGPAGSYRPYDEGLRRGVFITNETGQPLIGKVWPGSTAFPDFTNPTALAWWEDMVA" +
"EFHDQVPFDGMWIDMNEPSNFIRGSEDGCPNNELENPPYVPGVVGGTLQAATICASSHQFLSTHYNLHNLYG" +
"LTEAIASHRALVKARGTRPFVISRSTFAGHGRYAGHWTGDVWSSWEQLASSVPEILQFNLLGVPLVGADVCG" +
"FLGNTSEELCVRWTQLGAFYPFMRNHNSLLSLPQEPYSFSEPAQQAMRKALTLRYALLPHLYTLFHQAHVAG" +
"ETVARPLFLEFPKDSSTWTVDHQLLWGEALLITPVLQAGKAEVTGYFPLGTWYDLQTVPVEALGSLPPPPAA" +
"PREPAIHSEGQWVTLPAPLDTINVHLRAGYIIPLQGPGLTTTESRQQPMALAVALTKGGEARGELFWDDGES" +
"LEVLERGAYTQVIFLARNNTIVNELVRVTSEGAGLQLQKVTVLGVATAPQQVLSNGVPVSNFTYSPDTKVLD" +
"ICVSLLMGEQFLVSWC", "HUMAN", 100, TemplateID("5KZW", 'A'))
        except Exception as e:
             assert "has more bonds than this chemical element can form" in str(e)


    def test_3FDM(self):
        from hommod_rest.tasks import create_model
        path = create_model(
"MDGSGEQPRGGGPTSSEQIMKTGALLLQGFIQDRAGRMGGEAPELALDPVPQDASTKKLSECLKRIGDELDS" +
"NMELQRMIAAVDTDSPREVFFRVAADMFSDGNFNWGRVVALFYFASKLVLKALCTKVPELIRTIMGWTLDFL" +
"RERLLGWIQDQGGWDGLLSYFGTPTWQTVTIFVAGVLTASLTIWKKMG", "HUMAN", 100,
                            TemplateID("3FDM", 'A'))
        assert(len(path) > 0)

    def test_5NX2(self):
        from hommod_rest.tasks import create_model
        path = create_model(
"MMFRSDRMWSCHWKWKPSPLLFLFALYIMCVPHSVWGCANCRVVLSNPSGTFTSPCYPNDYPNSQACMWTLR" +
"APTGYIIQITFNDFDIEEAPNCIYDSLSLDNGESQTKFCGATAKGLSFNSSANEMHVSFSSDFSIQKKGFNA" +
"SYIRVAVSLRNQKVILPQTSDAYQVSVAKSISIPELSAFTLCFEATKVGHEDSDWTAFSYSNASFTQLLSFG" +
"KAKSGYFLSISDSKCLLNNALPVKEKEDIFAESFEQLCLVWNNSLGSIGVNFKRNYETVPCDSTISKVIPGN" +
"GKLLLGSNQNEIVSLKGDIYNFRLWNFTMNAKILSNLSCNVKGNVVDWQNDFWNIPNLALKAESNLSCGSYL" +
"IPLPAAELASCADLGTLCQATVNSPSTTPPTVTTNMPVTNRIDKQRNDGIIYRISVVIQNILRHPEVKVQSK" +
"VAEWLNSTFQNWNYTVYVVNISFHLSAGEDKIKVKRSLEDEPRLVLWALLVYNATNNTNLEGKIIQQKLLKN" +
"NESLDEGLRLHTVNVRQLGHCLAMEEPKGYYWPSIQPSEYVLPCPDKPGFSASRICFYNATNPLVTYWGPVD" +
"ISNCLKEANEVANQILNLTADGQNLTSANITNIVEQVKRIVNKEENIDITLGSTLMNIFSNILSSSDSDLLE" +
"SSSEALKTIDELAFKIDLNSTSHVNITTRNLALSVSSLLPGTNAISNFSIGLPSNNESYFQMDFESGQVDPL" +
"ASVILPPNLLENLSPEDSVLVRRAQFTFFNKTGLFQDVGPQRKTLVSYVMACSIGNITIQNLKDPVQIKIKH" +
"TRTQEVHHPICAFWDLNKNKSFGGWNTSGCVAHRDSDASETVCLCNHFTHFGVLMDLPRSASQLDARNTKVL" +
"TFISYIGCGISAIFSAATLLTYVAFEKLRRDYPSKILMNLSTALLFLNLLFLLDGWITSFNVDGLCIAVAVL" +
"LHFFLLATFTWMGLEAIHMYIALVKVFNTYIRRYILKFCIIGWGLPALVVSVVLASRNNNEVYGKESYGKEK" +
"GDEFCWIQDPVIFYVTCAGYFGVMFFLNIAMFIVVMVQICGRNGKRSNRTLREEVLRNLRSVVSLTFLLGMT" +
"WGFAFFAWGPLNIPFMYLFSIFNSLQGLFIFIFHCAMKENVQKQWRQHLCCGRFRLADNSDWSKTATNIIKK" +
"SSDNLGKSLSSSSIGSNSTYLTSKSKSSSTTYFKRNSHTDNVSYEHSFNKSGSLRQCFHGQVLVKTGPC",
        "HUMAN", 900, TemplateID("5NX2", 'A'))
        assert(len(path) > 0)

    def test_4as1(self):
        from hommod_rest.tasks import create_model
        path = create_model(
"MASVWQRLGFYASLLKRQLNGGPDVIKWERRVIPGCTRSIYSATGKWTKEYTLQTRKDVEKWWHQRIKEQAS" +
"KISEADKSKPKFYVLSMFPYPSGKLHMGHVRVYTISDTIARFQKMRGMQVINPMGWDAFGLPAENAAVERNL" +
"HPQSWTQSNIKHMRKQLDRLGLCFSWDREITTCLPDYYKWTQYLFIKLYEAGLAYQKEALVNWDPVDQTVLA" +
"NEQVDEHGCSWRSGAKVEQKYLRQWFIKTTAYAKAMQDALADLPEWYGIKGMQAHWIGDCVGCHLDFTLKVH" +
"GQATGEKLTAYTATPEAIYGTSHVAISPSHRLLHGHSSLKEALRMALVPGKDCLTPVMAVNMLTQQEVPVVI" +
"LAKADLEGSLDSKIGIPSTSSEDTILAQTLGLAYSEVIETLPDGTERLSSSAEFTGMTRQDAFLALTQKARG" +
"KRVGGDVTSDKLKDWLISRQRYWGTPIPIVHCPVCGPTPVPLEDLPVTLPNIASFTGKGGPPLAMASEWVNC" +
"SCPRCKGAAKRETDTMDTFVDSAWYYFRYTDPHNPHSPFNTAVADYWMPVDLYIGGKEHAVMHLFYARFFSH" +
"FCHDQKMVKHREPFHKLLAQGLIKGQTFRLPSGQYLQREEVDLTGSVPVHAKTKEKLEVTWEKMSKSKHNGV" +
"DPEEVVEQYGIDTIRLYILFAAPPEKDILWDVKTDALPGVLRWQQRLWTLTTRFIEARASGKSPQPQLLSNK" +
"EKAEARKLWEYKNSVISQVTTHFTEDFSLNSAISQLMGLSNALSQASQSVILHSPEFEDALCALMVMAAPLA" +
"PHVTSEIWAGLALVPRKLCAHYTWDASVLLQAWPAVDPEFLQQPEVVQMAVLINNKACGKIPVPQQVARDQD" +
"KVHEFVLQSELGVRLLQGRSIKKSFLSPRTALINFLVQD", "HUMAN", 113, TemplateID("4AS1", 'A'))
        assert(len(path) > 0)
