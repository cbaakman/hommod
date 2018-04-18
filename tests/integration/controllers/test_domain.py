import logging

from mock import patch
from nose.tools import ok_, with_setup

from hommod.default_settings import (INTERPRO_URL, BLASTP_EXE,
                                     FORBIDDEN_INTERPRO_DOMAINS, TEMPLATE_BLAST_DATABANK,
                                     DOMAIN_MIN_PERCENTAGE_COVERAGE, DOMAIN_MAX_MERGE_DISTANCE,
                                     DSSP_DIR, SIMILAR_RANGES_MIN_OVERLAP_PERCENTAGE,
                                     SIMILAR_RANGES_MAX_LENGTH_DIFFERENCE_PERCENTAGE,
                                     BLACKLIST_FILE_PATH, HIGHLY_HOMOLOGOUS_PERCENTAGE_IDENTITY,
                                     CACHE_REDIS_HOST, CACHE_REDIS_PORT, CACHE_REDIS_DB,
                                     CACHE_EXPIRATION_TIME, CACHE_LOCK_TIMEOUT)
from hommod.services.helpers.cache import cache_manager as cm
from hommod.controllers.domain import domain_aligner
from hommod.controllers.blast import blaster
from hommod.controllers.blacklist import blacklister
from hommod.services.interpro import interpro
from hommod.services.dssp import dssp
from hommod.models.template import TemplateID
from hommod.models.range import SequenceRange


_log = logging.getLogger(__name__)


def setup():
    blaster.blastp_exe = BLASTP_EXE
    interpro.url = INTERPRO_URL
    dssp.dssp_dir = DSSP_DIR
    blacklister.file_path = BLACKLIST_FILE_PATH
    domain_aligner.forbidden_interpro_domains = FORBIDDEN_INTERPRO_DOMAINS
    domain_aligner.similar_ranges_min_overlap_percentage = SIMILAR_RANGES_MIN_OVERLAP_PERCENTAGE
    domain_aligner.similar_ranges_max_length_difference_percentage = SIMILAR_RANGES_MAX_LENGTH_DIFFERENCE_PERCENTAGE
    domain_aligner.min_percentage_coverage = DOMAIN_MIN_PERCENTAGE_COVERAGE
    domain_aligner.template_blast_databank = TEMPLATE_BLAST_DATABANK
    domain_aligner.max_merge_distance = DOMAIN_MAX_MERGE_DISTANCE
    domain_aligner.highly_homologous_percentage_identity = HIGHLY_HOMOLOGOUS_PERCENTAGE_IDENTITY
    cm.redis_hostname = CACHE_REDIS_HOST
    cm.redis_port = CACHE_REDIS_PORT
    cm.redis_db = CACHE_REDIS_DB
    cm.expiration_time = CACHE_EXPIRATION_TIME
    cm.lock_timeout = CACHE_LOCK_TIMEOUT

def end():
    pass


@patch("hommod.services.interpro.interpro.get_domain_ranges")
@with_setup(setup, end)
def test_no_alignment_flip(mock_get_domain_ranges):
    seq = (
"MGKLVALVLLGVGLSLVGEMFLAFRERVNASREVEPVEPENCHLIEELESGSEDIDILPSGLAFISSGLKYP" +
"GMPNFAPDEPGKIFLMDLNEQNPRAQALEISGGFDKELFNPHGISIFIDKDNTVYLYVVNHPHMKSTVEIFK" +
"FEEQQRSLVYLKTIKHELLKSVNDIVVLGPEQFYATRDHYFTNSLLSFFEMILDLRWTYVLFYSPREVKVVA" +
"KGFCSANGITVSADQKYVYVADVAAKNIHIMEKHDNWDLTQLKVIQLGTLVDNLTVDPATGDILAGCHPNPM" +
"KLLNYNPEDPPGSEVLRIQNVLSEKPRVSTVYANNGSVLQGTSVASVYHGKILIGTVFHKTLYCEL")

    mock_get_domain_ranges.return_value = [SequenceRange(0, len(seq), seq)]

    alignments = domain_aligner.get_domain_alignments(seq)
    for alignment in alignments:
        _log.debug("got alignment {}".format(alignment))

        ok_(alignment.target_alignment.replace('-','') in seq)


@patch("hommod.services.interpro.interpro.get_domain_ranges")
@with_setup(setup, end)
def test_find_template(mock_get_domain_ranges):
    seq = (
"MGKLVALVLLGVGLSLVGEMFLAFRERVNASREVEPVEPENCHLIEELESGSEDIDILPSGLAFISSGLKYP" +
"GMPNFAPDEPGKIFLMDLNEQNPRAQALEISGGFDKELFNPHGISIFIDKDNTVYLYVVNHPHMKSTVEIFK" +
"FEEQQRSLVYLKTIKHELLKSVNDIVVLGPEQFYATRDHYFTNSLLSFFEMILDLRWTYVLFYSPREVKVVA" +
"KGFCSANGITVSADQKYVYVADVAAKNIHIMEKHDNWDLTQLKVIQLGTLVDNLTVDPATGDILAGCHPNPM" +
"KLLNYNPEDPPGSEVLRIQNVLSEKPRVSTVYANNGSVLQGTSVASVYHGKILIGTVFHKTLYCEL")

    mock_get_domain_ranges.return_value = [SequenceRange(0, len(seq), seq)]

    alignments = domain_aligner.get_domain_alignments(seq, require_resnum=190)
    ok_(any([ali.count_aligned_residues() > 300 for ali in alignments]))


@with_setup(setup, end)
def test_any_template():
    seq = ("GYVPAVVIGTGYGAAVSALRLGEAGVQTLMLEMGQLWNQPGPDGNIFCGMLNPDKRSS" +
           "WFKNRTEAPLGSFLWLDVVNRNIDPYAGVLDRVNYDQMSVYVGRGVGGGSLVNGGMAV" +
           "EPKRSYFEEILPRVDSSEMYDRYFPRANSMLRVNHIDTKWFEDTEWYKFARVSREQAG" +
           "KAGLGTVFVPNVYDFGYMQREAAGEVPKSALATEVIYGNNHGKQSLDKTYLAAALGTG" +
           "KVTIQTLHQVKTIRQTKDGGYALTVEQKDTDGKLLATKEISCRYLFLGAGSLGSTELL" +
           "VRARDTGTLPNLNSEVGAGWGPNGNIMTARANHMWNPTGAHQSSIPALGIDAWDNSDS" +
           "SVFAEIAPMPAGLETWVSLYLAITKNPQRGTFVYDAATDRAKLNWTRDQNAPAVNAAK" +
           "ALFDRINKANGTIYRYDLFGTQLKAFADDFCYNPLGGCVLGKATDDYGRVAGYKNLYV" +
           "TDGSLIPGSVGVNPFVTITALAERNVERIIKQDV")

    alignments = domain_aligner.get_domain_alignments(seq)
    ok_(len(alignments) > 0)


@with_setup(setup, end)
def test_4rh7_A():
    seq = ("MANGTADVRKLFIFTTTQNYFGLMSELWDQPLLCNCLEINNFLDDGNQMLLRVQRSDAGISFSN" +
           "TIEFGDTKDKVLVFFKLRPEVITDENLHDNILVSSMLESPISSLYQAVRQVFAPMLLKDQEWSR" +
           "NFDPKLQNLLSELEAGLGIVLRRSDTNLTKLKFKEDDTRGILTPSDEFQFWIEQAHRGNKQISK" +
           "ERANYFKELFETIAREFYNLDSLSLLEVVDLVETTQDVVDDVWRQTEHDHYPESRMLHLLDIIG" +
           "GSFGRFVQKKLGTLNLWEDPYYLVKESLKAGISICEQWVIVCNHLTGQVWQRYVPHPWKNEKYF" +
           "PETLDKLGKRLEEVLAIRTIHEKFLYFLPASEEKIICLTRVFEPFTGLNPVQYNPYTEPLWKAA" +
           "VSQYEKIIAPAEQKIAGKLKNYISEIQDSPQQLLQAFLKYKELVKRPTISKELMLERETLLARL" +
           "VDSIKDFRLDFENRCRGIPGDASGPLSGKNLSEVVNSIVWVRQLELKVDDTIKIAEALLSDLPG" +
           "FRCFHQSAKDLLDQLKLYEQEQFDDWSRDIQSGLSDSRSGLCIEASSRIMELDSNDGLLKVHYS" +
           "DRLVILLREVRQLSALGFVIPAKIQQVANIAQKFCKQAIILKQVAHFYNSIDQQMIQSQRPMML" +
           "QSALAFEQIIKNSKAGSGGKSQITWDNPKELEGYIQKLQNAAERLATENRKLRKWHTTFCEKVV" +
           "VLMNIDLLRQQQRWKDGLQELRTGLATVEAQGFQASDMHAWKQHWNHQLYKALEHQYQMGLEAL" +
           "NENLPEINIDLTYKQGRLQFRPPFEEIRAKYYREMKRFIGIPNQFKGVGEAGDESIFSIMIDRN" +
           "ASGFLTIFSKAEDLFRRLSAVLHQHKEWIVIGQVDMEALVEKHLFTVHDWEKNFKALKIKGKEV" +
           "ERLPSAVKVDCLNINCNPVKTVIDDLIQKLFDLLVLSLKKSIQAHLHEIDTFVTEAMEVLTIMP" +
           "QSVEEIGDANLQYSKLQERKPEILPLFQEAEDKNRLLRTVAGGGLETISNLKAKWDKFELMMES" +
           "HQLMIKDQIEVMKGNVKSRLQIYYQELEKFKARWDQLKPGDDVIETGQHNTLDKSAKLIKEKKI" +
           "EFDDLEVTRKKLVDDCHHFRLEEPNFSLASSISKDIESCAQIWAFYEEFQQGFQEMANEDWITF" +
           "RTKTYLFEEFLMNWHDRLRKVEEHSVMTVKLQSEVDKYKIVIPILKYVRGEHLSPDHWLDLFRL" +
           "LGLPRGTSLEKLLFGDLLRVADTIVAKAADLKDLNSRAQGEVTIREALRELDLWGVGAVFTLID" +
           "YEDSQSRTMKLIKDWKDIVNQVGDNRCLLQSLKDSPYYKGFEDKVSIWERKLAELDEYLQNLNH" +
           "IQRKWVYLEPIFGRGALPKEQTRFNRVDEDFRSIMTDIKKDNRVTTLTTHAGIRNSLLTILDQL" +
           "QRCQKSLNEFLEEKRSAFPRFYFIGDDDLLEILGQSTNPSVIQSHLKKLFAGINSVCFDEKSKH" +
           "ITAMKSLEGEVVPFKNKVPLSNNVETWLNDLALEMKKTLEQLLKECVTTGRSSQGAVDPSLFPS" +
           "QILCLAEQIKFTEDVENAIKDHSLHQIETQLVNKLEQYTNIDTSSEDPGNTESGILELKLKALI" +
           "LDIIHNIDVVKQLNQIQVHTTEDWAWKKQLRFYMKSDHTCCVQMVDSEFQYTYEYQGNASKLVY" +
           "TPLTDKCYLTLTQAMKMGLGGNPYGPAGTGKTESVKALGGLLGRQVLVFNCDEGIDVKSMGRIF" +
           "VGLVKCGAWGCFDEFNRLEESVLSAVSMQIQTIQDALKNHRTVCELLGKEVEVNSNSGIFITMN" +
           "PAGKGYGGRQKLPDNLKQLFRPVAMSHPDNELIAEVILYSEGFKDAKVLSRKLVAIFNLSRELL" +
           "TPQQHYDWGLRALKTVLRGSGNLLRQLNKSGTTQNANESHIVVQALRLNTMSKFTFTDCTRFDA" +
           "LIKDVFPGIELKEVEYDELSAALKQVFEEANYEIIPNQIKKALELYEQLCQRMGVVIVGPSGAG" +
           "KSTLWRMLRAALCKTGKVVKQYTMNPKAMPRYQLLGHIDMDTREWSDGVLTNSARQVVREPQDV" +
           "SSWIICDGDIDPEWIESLNSVLDDNRLLTMPSGERIQFGPNVNFVFETHDLSCASPATISRMGM" +
           "IFLSDEETDLNSLIKSWLRNQPAEYRNNLENWIGDYFEKALQWVLKQNDYVVETSLVGTVMNGL" +
           "SHLHGCRDHDEFIINLIRGLGGNLNMKSRLEFTKEVFHWARESPPDFHKPMDTYYDSTRGRLAT" +
           "YVLKKPEDLTADDFSNGLTLPVIQTPDMQRGLDYFKPWLSSDTKQPFILVGPEGCGKGMLLRYA" +
           "FSQLRSTQIATVHCSAQTTSRHLLQKLSQTCMVISTNTGRVYRPKDCERLVLYLKDINLPKLDK" +
           "WGTSTLVAFLQQVLTYQGFYDENLEWVGLENIQIVASMSAGGRLGRHKLTTRFTSIVRLCSIDY" +
           "PEREQLQTIYGAYLEPVLHKNLKNHSIWGSSSKIYLLAGSMVQVYEQVRAKFTVDDYSHYFFTP" +
           "CILTQWVLGLFRYDLEGGSSNHPLDYVLEIVAYEARRLFRDKIVGAKELHLFDIILTSVFQGDW" +
           "GSDILDNMSDSFYVTWGARHNSGARAAPGQPLPPHGKPLGKLNSTDLKDVIKKGLIHYGRDNQN" +
           "LDILLFHEVLEYMSRIDRVLSFPGGSLLLAGRSGVGRRTITSLVSHMHGAVLFSPKISRGYELK" +
           "QFKNDLKHVLQLAGIEAQQVVLLLEDYQFVHPTFLEMINSLLSSGEVPGLYTLEELEPLLLPLK" +
           "DQASQDGFFGPVFNYFTYRIQQNLHIVLIMDSANSNFMINCESNPALHKKCQVLWMEGWSNSSM" +
           "KKIPEMLFSETGGGEKYNDKKRKEEKKKNSVDPDFLKSFLLIHESCKAYGATPSRYMTFLHVYS" +
           "AISSSKKKELLKRQSHLQAGVSKLNEAKALVDELNRKAGEQSVLLKTKQDEADAALQMITVSMQ" +
           "DASEQKTELERLKHRIAEEVVKIEERKNKIDDELKEVQPLVNEAKLAVGNIKPESLSEIRSLRM" +
           "PPDVIRDILEGVLRLMGIFDTSWVSMKSFLAKRGVREDIATFDARNISKEIRESVEELLFKNKG" +
           "SFDPKNAKRASTAAAPLAAWVKANIQYSHVLERIHPLETEQAGLESNLKKTEDRKRKLEELLNS" +
           "VGQKVSELKEKFQSRTSEAAKLEAEVSKAQETIKAAEVLINQLDREHKRWNAQVVEITEELATL" +
           "PKRAQLAAAFITYLSAAPESLRKTCLEEWTKSAGLEKFDLRRFLCTESEQLIWKSEGLPSDDLS" +
           "IENALVILQSRVCPFLIDPSSQATEWLKTHLKDSRLEVINQQDSNFITALELAVRFGKTLIIQE" +
           "MDGVEPVLYPLLRRDLVAQGPRYVVQIGDKIIDYNEEFRLFLSTRNPNPFIPPDAASIVTEVNF" +
           "TTTRSGLRGQLLALTIQHEKPDLEEQKTKLLQQEEDKKIQLAKLEESLLETLATSQGNILENKD" +
           "LIESLNQTKASSALIQESLKESYKLQISLDQERDAYLPLAESASKMYFIISDLSKINNMYRFSL" +
           "AAFLRLFQRALQNKQDSENTEQRIQSLISSLQHMVYEYICRCLFKADQLMFALHFVRGMHPELF" +
           "QENEWDTFTGVVVGDMLRKADSQQKIRDQLPSWIDQERSWAVATLKIALPSLYQTLCFEDAALW" +
           "RTYYNNSMCEQEFPSILAKKVSLFQQILVVQALRPDRLQSAMALFACKTLGLKEVSPLPLNLKR" +
           "LYKETLEIEPILIIISPGADPSQELQELANAERSGECYHQVAMGQGQADLAIQMLKECARNGDW" +
           "LCLKNLHLVVSWLPVLEKELNTLQPKDTFRLWLTAEVHPNFTPILLQSSLKITYESPPGLKKNL" +
           "MRTYESWTPEQISKKDNTHRAHALFSLAWFHAACQERRNYIPQGWTKFYEFSLSDLRAGYNIID" +
           "RLFDGAKDVQWEFVHGLLENAIYGGRIDNYFDLRVLQSYLKQFFNSSVIDVFNQRNKKSIFPYS" +
           "VSLPQSCSILDYRAVIEKIPEDDKPSFFGLPANIARSSQRMISSQVISQLRILGRSITAGSKFD" +
           "REIWSNELSPVLNLWKKLNQNSNLIHQKVPPPNDRQGSPILSFIILEQFNAIRLVQSVHQSLAA" +
           "LSKVIRGTTLLSSEVQKLASALLNQKCPLAWQSKWEGPEDPLQYLRGLVARALAIQNWVDKAEK" +
           "QALLSETLDLSELFHPDTFLNALRQETARAVGRSVDSLKFVASWKGRLQEAKLQIKISGLLLEG" +
           "CSFDGNQLSENQLDSPSVSSVLPCFMGWIPQDACGPYSPDECISLPVYTSAERDRVVTNIDVPC" +
           "GGNQDQWIQCGAALFLKNQ")

    template_id = TemplateID('4RH7', 'A')

    alignments = domain_aligner.get_domain_alignments(seq, template_id=template_id)
    ok_(len(alignments) > 0)


@with_setup(setup, end)
def test_2ypd_A():
    seq = ("MADAAASPVGKRLLLLFADTAASASASAPAAAAASGDPGPALRTRAWRAGTVRAMSGAVPQDLA" +
           "IFVEFDGCNWKQHSWVKVHAEEVIVLLLEGSLVWAPREDPVLLQGIRVSIAQWPALTFTPLVDK" +
           "LGLGSVVPVEYLLDRELRFLSDANGLHLFQMGTDSQNQILLEHAALRETVNALISDQKLQEIFS" +
           "RGPYSVQGHRVKIYQPEGEEGWLYGVVSHQDSITRLMEVSVTESGEIKSVDPRLIHVMLMDNST" +
           "PQSEGGTLKAVKSSKGKKKRESIEGKDGRRRKSASDSGCDPASKKLKGDRGEVDSNGSDGGEAS" +
           "RGPWKGGNASGEPGLDQRAKQPPSTFVPQINRNIRFATYTKENGRTLVVQDEPVGGDTPASFTP" +
           "YSTATGQTPLAPEVGGAENKEAGKTLEQVGQGIVASAAVVTTASSTPNTVRISDTGLAAGTVPE" +
           "KQKGSRSQASGENSRNSILASSGFGAPLPSSSQPLTFGSGRSQSNGVLATENKPLGFSFGCSSA" +
           "QEAQKDTDLSKNLFFQCMSQTLPTSNYFTTVSESLADDSSSRDSFKQSLESLSSGLCKGRSVLG" +
           "TDTKPGSKAGSSVDRKVPAESMPTLTPAFPRSLLNARTPENHENLFLQPPKLSREEPSNPFLAF" +
           "VEKVEHSPFSSFASQASGSSSSATTVTSKVAPSWPESHSSADSASLAKKKPLFITTDSSKLVSG" +
           "VLGSALTSGGPSLSAMGNGRSSSPTSSLTQPIEMPTLSSSPTEERPTVGPGQQDNPLLKTFSNV" +
           "FGRHSGGFLSSPADFSQENKAPFEAVKRFSLDERSLACRQDSDSSTNSDLSDLSDSEEQLQAKT" +
           "GLKGIPEHLMGKLGPNGERSAELLLGKSKGKQAPKGRPRTAPLKVGQSVLKDVSKVKKLKQSGE" +
           "PFLQDGSCINVAPHLHKCRECRLERYRKFKEQEQDDSTVACRFFHFRRLIFTRKGVLRVEGFLS" +
           "PQQSDPDAMNLWIPSSSLAEGIDLETSKYILANVGDQFCQLVMSEKEAMMMVEPHQKVAWKRAV" +
           "RGVREMCDVCETTLFNIHWVCRKCGFGVCLDCYRLRKSRPRSETEEMGDEEVFSWLKCAKGQSH" +
           "EPENLMPTQIIPGTALYNIGDMVHAARGKWGIKANCPCISRQNKSVLRPAVTNGMSQLPSINPS" +
           "ASSGNETTFSGGGGPAPVTTPEPDHVPKADSTDIRSEEPLKTDSSASNSNSELKAIRPPCPDTA" +
           "PPSSALHWLADLATQKAKEETKEAGSLRSVLNKESHSPFGLDSFNSTAKVSPLTPKLFNSLLLG" +
           "PTASNNKTEGSSLRDLLHSGPGKLPQTPLDTGIPFPPVFSTSSAGVKSKASLPNFLDHIIASVV" +
           "ENKKTSDASKRACNLTDTQKEVKEMVMGLNVLDPHTSHSWLCDGRLLCLHDPSNKNNWKIFREC" +
           "WKQGQPVLVSGVHKKLKSELWKPEAFSQEFGDQDVDLVNCRNCAIISDVKVRDFWDGFEIICKR" +
           "LRSEDGQPMVLKLKDWPPGEDFRDMMPTRFEDLMENLPLPEYTKRDGRLNLASRLPSYFVRPDL" +
           "GPKMYNAYGLITAEDRRVGTTNLHLDVSDAVNVMVYVGIPIGEGAHDEEVLKTIDEGDADEVTK" +
           "QRIHDGKEKPGALWHIYAAKDAEKIRELLRKVGEEQGQENPPDHDPIHDQSWYLDQTLRKRLYE" +
           "EYGVQGWAIVQFLGDAVFIPAGAPHQVHNLYSCIKVAEDFVSPEHVKHCFRLTQEFRHLSNTHT" +
           "NHEDKLQVKNIIYHAVKDAVGTLKAHESKLARS")

    template_id = TemplateID('2YPD', 'A')

    alignments = domain_aligner.get_domain_alignments(seq, template_id=template_id)
    ok_(alignments[0].range.get_length() <= len(seq))


@with_setup(setup, end)
def test_3ly6_A():
    seq = ("MGQGEPSQRSTGLAGLYAAPAASPVFIKGSGMDALGIKSCDFQAARNNEEHHTKALSSRRLFVR" +
           "RGQPFTIILYFRAPVRAFLPALKKVALTAQTGEQPSKINRTQATFPISSLGDRKWWSAVVEERD" +
           "AQSWTISVTTPADAVIGHYSLLLQVSGRKQLLLGQFTLLFNPWNREDAVFLKNEAQRMEYLLNQ" +
           "NGLIYLGTADCIQAESWDFGQFEGDVIDLSLRLLSKDKQVEKWSQPVHVARVLGALLHFLKEQR" +
           "VLPTPQTQATQEGALLNKRRGSVPILRQWLTGRGRPVYDGQAWVLAAVACTVLRCLGIPARVVT" +
           "TFASAQGTGGRLLIDEYYNEEGLQNGEGQRGRIWIFQTSTECWMTRPALPQGYDGWQILHPSAP" +
           "NGGGVLGSCDLVVRAVKEGTLGLTPAVSDLFAAINASCVVWKCCEDGTLELTDSNTKYVGNNIS" +
           "TKGVGSDRCEDITQNYKYPEGSLQEKEVLERVEKEKMEREKDNGIRPPSLETASPLYLLLKAPS" +
           "SLPLRGDAQISVTLVNHSEQEKAVQLAIGVQAVHYNGVLAAKLWRKKLHLTLSANLEKIITIGL" +
           "FFSNFERNPPENTFLRLTAMATHSESNLSCFAQEDIAICRPHLAIKMPEKAEQYQPLTASVSLQ" +
           "NSLDAPMEDCVISILGRGLIHRERSYRFRSVWPENTMCAKFQFTPTHVGLQRLTVEVDCNMFQN" +
           "LTNYKSVTVVAPELSA")

    template_id = TemplateID('3LY6', 'A')

    alignments = domain_aligner.get_domain_alignments(seq, template_id=template_id)

    ok_(alignments[0].range.get_length() <= len(seq))