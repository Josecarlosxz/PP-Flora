/* ============================================================
   BioSistema — Dados do Mapa Interativo (Flora)
   Vegetação e planta principal por estado / bioma do Brasil
   ------------------------------------------------------------
   Para editar: altere os campos de cada estado abaixo.
   ============================================================ */

/* Cores oficiais de cada bioma (usadas no mapa e na legenda) */
const BIOMAS = {
  "Amazônia":      { cor: "#1b7a3d", emoji: "🌳" },
  "Cerrado":       { cor: "#d9a521", emoji: "🌾" },
  "Caatinga":      { cor: "#b5451f", emoji: "🌵" },
  "Mata Atlântica":{ cor: "#1f8a8a", emoji: "🌲" },
  "Pantanal":      { cor: "#7b52ab", emoji: "🐊" },
  "Pampa":         { cor: "#4a6fa5", emoji: "🐎" }
};

/* ------------------------------------------------------------
   DADOS POR ESTADO
   sigla -> { nome, bioma, planta, plantaIcon, plantaDesc,
              vegetacao, vegetacaoIcon, vegetacaoDesc }
   ------------------------------------------------------------ */
const ESTADOS = {

  /* ================= NORTE ================= */
  AC: { nome: "Acre", bioma: "Amazônia",
    planta: "Seringueira", plantaIcon: "🌳",
    plantaDesc: "Árvore da borracha nativa da Amazônia, base do ciclo econômico e cultural do Acre.",
    vegetacao: "Floresta Ombrófila Aberta", vegetacaoIcon: "🌴",
    vegetacaoDesc: "Floresta tropical úmida com palmeiras e bambus, típica do oeste amazônico." },

  AP: { nome: "Amapá", bioma: "Amazônia",
    planta: "Vitória-régia", plantaIcon: "🌺",
    plantaDesc: "Grande planta aquática de folhas circulares, comum em rios e igarapés amazônicos.",
    vegetacao: "Floresta de Várzea e Igapó", vegetacaoIcon: "🌊",
    vegetacaoDesc: "Vegetação inundável que acompanha os rios nas cheias sazonais." },

  AM: { nome: "Amazonas", bioma: "Amazônia",
    planta: "Castanheira-do-pará", plantaIcon: "🌰",
    plantaDesc: "Árvore gigante da floresta amazônica, produtora da castanha-do-pará.",
    vegetacao: "Floresta Ombrófila Densa", vegetacaoIcon: "🌳",
    vegetacaoDesc: "A maior floresta tropical do planeta, com altíssima biodiversidade." },

  PA: { nome: "Pará", bioma: "Amazônia",
    planta: "Açaizeiro", plantaIcon: "🌴",
    plantaDesc: "Palmeira típica dos igapós e várzeas, símbolo da cultura e da economia paraense.",
    vegetacao: "Floresta Densa e Manguezais", vegetacaoIcon: "🌴",
    vegetacaoDesc: "Floresta de terra firme e manguezais no litoral paraense." },

  RO: { nome: "Rondônia", bioma: "Amazônia",
    planta: "Andiroba", plantaIcon: "🌳",
    plantaDesc: "Árvore amazônica de óleo medicinal, tradicionalmente usada por povos da floresta.",
    vegetacao: "Floresta Amazônica e Cerrado", vegetacaoIcon: "🌳",
    vegetacaoDesc: "Transição entre floresta úmida e áreas de cerrado no sul do estado." },

  RR: { nome: "Roraima", bioma: "Amazônia",
    planta: "Buriti", plantaIcon: "🌴",
    plantaDesc: "Palmeira de brejos e áreas alagadas, marcante na paisagem do lavrado roraimense.",
    vegetacao: "Lavrado (Savana Amazônica)", vegetacaoIcon: "🌾",
    vegetacaoDesc: "Campos abertos de savana intercalados com florestas de galeria." },

  TO: { nome: "Tocantins", bioma: "Cerrado",
    planta: "Ipê-amarelo", plantaIcon: "🌼",
    plantaDesc: "Árvore de floração amarela vibrante, uma das mais emblemáticas do Cerrado brasileiro.",
    vegetacao: "Cerrado", vegetacaoIcon: "🌾",
    vegetacaoDesc: "Savana brasileira com árvores retorcidas, arbustos e gramíneas." },

  /* ================= NORDESTE ================= */
  MA: { nome: "Maranhão", bioma: "Cerrado",
    planta: "Babaçu", plantaIcon: "🌴",
    plantaDesc: "Palmeira de grande importância social e econômica, base do extrativismo maranhense.",
    vegetacao: "Mata dos Cocais (Babaçu)", vegetacaoIcon: "🌴",
    vegetacaoDesc: "Floresta de transição dominada por palmeiras de babaçu e carnaúba." },

  PI: { nome: "Piauí", bioma: "Caatinga",
    planta: "Carnaúba", plantaIcon: "🌴",
    plantaDesc: "Conhecida como \"árvore da vida\", fornece cera, fibras e alimento no sertão piauiense.",
    vegetacao: "Caatinga e Cerrado", vegetacaoIcon: "🌵",
    vegetacaoDesc: "Vegetação xerófila adaptada à seca, com cactos e arbustos espinhosos." },

  CE: { nome: "Ceará", bioma: "Caatinga",
    planta: "Mandacaru", plantaIcon: "🌵",
    plantaDesc: "Cacto colunar símbolo da Caatinga, resistente à seca e presente na cultura cearense.",
    vegetacao: "Caatinga", vegetacaoIcon: "🌵",
    vegetacaoDesc: "Único bioma exclusivamente brasileiro, resistente à longa estiagem." },

  RN: { nome: "Rio Grande do Norte", bioma: "Caatinga",
    planta: "Xique-xique", plantaIcon: "🌵",
    plantaDesc: "Cacto ramificado típico do sertão potiguar, usado até como forragem para o gado.",
    vegetacao: "Caatinga e Restinga", vegetacaoIcon: "🌵",
    vegetacaoDesc: "Vegetação seca do sertão e restingas arenosas no litoral." },

  PB: { nome: "Paraíba", bioma: "Caatinga",
    planta: "Umbuzeiro", plantaIcon: "🌳",
    plantaDesc: "Árvore de raízes que armazenam água, dá o umbu e é chamada de \"pai do sertão\".",
    vegetacao: "Caatinga e Mata Atlântica", vegetacaoIcon: "🌳",
    vegetacaoDesc: "Transição entre o sertão seco e remanescentes de floresta atlântica." },

  PE: { nome: "Pernambuco", bioma: "Caatinga",
    planta: "Facheiro", plantaIcon: "🌵",
    plantaDesc: "Cacto de porte alto e colunar, comum no sertão pernambucano.",
    vegetacao: "Caatinga e Mata Atlântica", vegetacaoIcon: "🌳",
    vegetacaoDesc: "Mosaico de caatinga no interior e floresta atlântica na zona da mata." },

  AL: { nome: "Alagoas", bioma: "Mata Atlântica",
    planta: "Coqueiro", plantaIcon: "🌴",
    plantaDesc: "Palmeira característica do litoral alagoano, marca registrada das praias do estado.",
    vegetacao: "Mata Atlântica e Manguezais", vegetacaoIcon: "🌳",
    vegetacaoDesc: "Floresta costeira e manguezais que abrigam rica vida marinha." },

  SE: { nome: "Sergipe", bioma: "Mata Atlântica",
    planta: "Mangue-vermelho", plantaIcon: "🌿",
    plantaDesc: "Árvore de raízes aéreas que forma os manguezais dos estuários sergipanos.",
    vegetacao: "Mata Atlântica e Manguezais", vegetacaoIcon: "🌳",
    vegetacaoDesc: "Remanescentes de floresta atlântica e ecossistemas de mangue." },

  BA: { nome: "Bahia", bioma: "Caatinga",
    planta: "Licuri", plantaIcon: "🌴",
    plantaDesc: "Palmeira do sertão baiano cujos frutos são o principal alimento da arara-azul-de-lear.",
    vegetacao: "Caatinga, Cerrado e Mata Atlântica", vegetacaoIcon: "🌵",
    vegetacaoDesc: "Estado com três grandes biomas, do sertão seco ao litoral úmido." },

  /* ================= CENTRO-OESTE ================= */
  MT: { nome: "Mato Grosso", bioma: "Pantanal",
    planta: "Ipê-roxo", plantaIcon: "🌸",
    plantaDesc: "Árvore de floração roxa intensa, presente nas paisagens do Pantanal mato-grossense.",
    vegetacao: "Pantanal, Cerrado e Amazônia", vegetacaoIcon: "🌾",
    vegetacaoDesc: "Encontro de três biomas, com a maior planície alagável do mundo." },

  MS: { nome: "Mato Grosso do Sul", bioma: "Pantanal",
    planta: "Aguapé", plantaIcon: "🌱",
    plantaDesc: "Planta aquática flutuante que cobre lagoas e baías do Pantanal sul-mato-grossense.",
    vegetacao: "Pantanal e Cerrado", vegetacaoIcon: "🌾",
    vegetacaoDesc: "Planície inundável com rica vegetação aquática e campos sazonais." },

  GO: { nome: "Goiás", bioma: "Cerrado",
    planta: "Pequizeiro", plantaIcon: "🌳",
    plantaDesc: "Árvore do Cerrado cujo fruto, o pequi, é símbolo da culinária goiana.",
    vegetacao: "Cerrado", vegetacaoIcon: "🌾",
    vegetacaoDesc: "Savana com árvores tortuosas, cascas grossas e raízes profundas." },

  DF: { nome: "Distrito Federal", bioma: "Cerrado",
    planta: "Barbatimão", plantaIcon: "🌿",
    plantaDesc: "Arbusto medicinal do Cerrado, tradicionalmente usado como cicatrizante.",
    vegetacao: "Cerrado", vegetacaoIcon: "🌾",
    vegetacaoDesc: "Berço do Cerrado, com áreas de proteção como a Reserva do IBGE." },

  /* ================= SUDESTE ================= */
  MG: { nome: "Minas Gerais", bioma: "Cerrado",
    planta: "Sempre-viva", plantaIcon: "🌸",
    plantaDesc: "Flor típica dos campos rupestres mineiros, famosa por não murchar após colhida.",
    vegetacao: "Cerrado e Mata Atlântica", vegetacaoIcon: "🌳",
    vegetacaoDesc: "Mosaico de cerrado, campos de altitude e floresta atlântica." },

  ES: { nome: "Espírito Santo", bioma: "Mata Atlântica",
    planta: "Pau-brasil", plantaIcon: "🌳",
    plantaDesc: "Árvore que deu nome ao país, hoje rara na Mata Atlântica que ainda a abriga.",
    vegetacao: "Mata Atlântica e Restinga", vegetacaoIcon: "🌳",
    vegetacaoDesc: "Floresta costeira, restingas e manguezais ao longo do litoral." },

  RJ: { nome: "Rio de Janeiro", bioma: "Mata Atlântica",
    planta: "Jequitibá-rosa", plantaIcon: "🌳",
    plantaDesc: "Uma das maiores árvores da Mata Atlântica, com exemplares centenários na Floresta da Tijuca.",
    vegetacao: "Mata Atlântica", vegetacaoIcon: "🌳",
    vegetacaoDesc: "Floresta tropical úmida, uma das mais ricas e ameaçadas do planeta." },

  SP: { nome: "São Paulo", bioma: "Mata Atlântica",
    planta: "Jacarandá-mimoso", plantaIcon: "💜",
    plantaDesc: "Árvore de flores lilás que colore as ruas paulistas na primavera.",
    vegetacao: "Mata Atlântica e Cerrado", vegetacaoIcon: "🌳",
    vegetacaoDesc: "Floresta atlântica no litoral e cerrado no interior do estado." },

  /* ================= SUL ================= */
  PR: { nome: "Paraná", bioma: "Mata Atlântica",
    planta: "Araucária", plantaIcon: "🌲",
    plantaDesc: "Pinheiro nativo símbolo do Paraná, característico da Mata de Araucárias.",
    vegetacao: "Floresta com Araucária", vegetacaoIcon: "🌲",
    vegetacaoDesc: "Floresta de pinheiros araucária, marca registrada do planalto sulista." },

  SC: { nome: "Santa Catarina", bioma: "Mata Atlântica",
    planta: "Erva-mate", plantaIcon: "🌿",
    plantaDesc: "Arbusto nativo da mata com araucárias, base histórica da economia catarinense.",
    vegetacao: "Floresta com Araucária e Restinga", vegetacaoIcon: "🌲",
    vegetacaoDesc: "Mata de araucárias no planalto e restingas no litoral catarinense." },

  RS: { nome: "Rio Grande do Sul", bioma: "Pampa",
    planta: "Butiá", plantaIcon: "🌴",
    plantaDesc: "Palmeira baixa e resistente, espalhada pelos campos nativos do Pampa gaúcho.",
    vegetacao: "Pampa (Campos Sulinos)", vegetacaoIcon: "🌾",
    vegetacaoDesc: "Campos nativos de gramíneas, único bioma restrito a um só estado." }
};

/* ------------------------------------------------------------
   MAPA DE TÍTULOS DA WIKIPÉDIA
   ------------------------------------------------------------
   Alguns nomes usados no mapa não são exatamente o título do
   artigo na Wikipédia. Este mapa traduz o nome exibido para o
   título correto, garantindo que a página de detalhes encontre
   a imagem real e o texto completo.

   Se um nome não estiver aqui, o detalhe.js usa o próprio nome.
   ------------------------------------------------------------ */
const WIKI_TITULOS = {

  /* ---- PLANTAS ---- */
  "Seringueira":          "Hevea brasiliensis",
  "Vitória-régia":        "Victoria amazonica",
  "Castanheira-do-pará":  "Bertholletia excelsa",
  "Açaizeiro":            "Euterpe oleracea",
  "Andiroba":             "Carapa guianensis",
  "Buriti":               "Mauritia flexuosa",
  "Ipê-amarelo":          "Handroanthus albus",
  "Babaçu":               "Attalea speciosa",
  "Carnaúba":             "Copernicia prunifera",
  "Mandacaru":            "Cereus jamacaru",
  "Xique-xique":          "Pilosocereus gounellei",
  "Umbuzeiro":            "Spondias tuberosa",
  "Facheiro":             "Pilosocereus pachycladus",
  "Coqueiro":             "Cocos nucifera",
  "Mangue-vermelho":      "Rhizophora mangle",
  "Licuri":               "Syagrus coronata",
  "Ipê-roxo":             "Handroanthus impetiginosus",
  "Aguapé":               "Eichhornia crassipes",
  "Pequizeiro":           "Caryocar brasiliense",
  "Barbatimão":           "Stryphnodendron adstringens",
  "Sempre-viva":          "Syngonanthus elegans",
  "Pau-brasil":           "Paubrasilia echinata",
  "Jequitibá-rosa":       "Cariniana legalis",
  "Jacarandá-mimoso":     "Jacaranda mimosifolia",
  "Araucária":            "Araucaria angustifolia",
  "Erva-mate":            "Ilex paraguariensis",
  "Butiá":                "Butia odorata",

  /* ---- VEGETAÇÃO ---- */
  "Floresta Ombrófila Aberta":          "Floresta ombrófila aberta",
  "Floresta de Várzea e Igapó":         "Floresta de várzea",
  "Floresta Ombrófila Densa":           "Floresta ombrófila densa",
  "Floresta Densa e Manguezais":        "Manguezal",
  "Floresta Amazônica e Cerrado":       "Amazônia",
  "Lavrado (Savana Amazônica)":         "Lavrado",
  "Cerrado":                            "Cerrado",
  "Mata dos Cocais (Babaçu)":           "Mata dos cocais",
  "Caatinga e Cerrado":                 "Caatinga",
  "Caatinga":                           "Caatinga",
  "Caatinga e Restinga":                "Restinga",
  "Caatinga e Mata Atlântica":          "Caatinga",
  "Mata Atlântica e Manguezais":        "Mata Atlântica",
  "Mata Atlântica":                     "Mata Atlântica",
  "Caatinga, Cerrado e Mata Atlântica": "Caatinga",
  "Pantanal, Cerrado e Amazônia":       "Pantanal",
  "Pantanal e Cerrado":                 "Pantanal",
  "Cerrado e Mata Atlântica":           "Cerrado",
  "Mata Atlântica e Restinga":          "Mata Atlântica",
  "Mata Atlântica e Cerrado":           "Mata Atlântica",
  "Floresta com Araucária":             "Floresta ombrófila mista",
  "Floresta com Araucária e Restinga":  "Floresta ombrófila mista",
  "Pampa (Campos Sulinos)":             "Pampa"
};