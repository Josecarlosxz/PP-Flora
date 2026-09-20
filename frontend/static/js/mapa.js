/* ============================================================
   BioSistema — Mapa Interativo (Fauna & Flora do Brasil)
   Tecnologia: Leaflet + GeoJSON (sem tile layer de base)
   Depende de: mapa_data.js (BIOMAS e ESTADOS)
   ============================================================ */

document.addEventListener("DOMContentLoaded", function () {

  const elMapa = document.getElementById("mapaBrasil");
  if (!elMapa) return; // segurança: só roda se o mapa existir na página

  /* ----------------------------------------------------------
     1) Inicializa o mapa
     ---------------------------------------------------------- */
  const limitesBrasil = L.latLngBounds(
    [-35, -75], // sudoeste
    [ 7, -32]   // nordeste
  );

  const mapa = L.map("mapaBrasil", {
    center: [-14.5, -52],
    zoom: 4,
    minZoom: 3,
    maxZoom: 9,
    zoomControl: true,
    scrollWheelZoom: false, // evita "sequestrar" o scroll da página
    maxBounds: limitesBrasil,       // impede arrastar para ver outros países
    maxBoundsViscosity: 1.0
  });

  /* ----------------------------------------------------------
     2) Camada base
     ----------------------------------------------------------
     Sem tile layer (OpenStreetMap) de propósito: o mapa-múndi de
     fundo deixava os países vizinhos muito visíveis. Sem essa
     camada, só aparecem os estados do Brasil (GeoJSON abaixo),
     e o resto fica com a cor de fundo definida em mapa.css
     (#mapaBrasil { background: ... }).
     ---------------------------------------------------------- */

  /* ----------------------------------------------------------
     3) Legenda de biomas
     ---------------------------------------------------------- */
  const elLegenda = document.getElementById("mapaLegenda");
  if (elLegenda) {
    Object.entries(BIOMAS).forEach(([nome, cfg]) => {
      const item = document.createElement("div");
      item.className = "legenda-item";
      item.innerHTML =
        `<span class="legenda-cor" style="background:${cfg.cor}"></span>${cfg.emoji} ${nome}`;
      elLegenda.appendChild(item);
    });
  }

  /* ----------------------------------------------------------
     4) Estilo de cada estado conforme o bioma
     ----------------------------------------------------------
     Quando os limites REAIS dos biomas (passo 7.3) carregam com
     sucesso, os estados passam a ficar "transparentes" (só a
     fronteira fina aparece) — quem colore o mapa nesse caso é a
     camada de biomas reais, por baixo. Se aquela camada falhar
     (sem internet, serviço fora do ar etc.), os estados voltam a
     ser coloridos como antes, por bioma predominante.
     ---------------------------------------------------------- */
  let biomasReaisCarregados = false;

  function estilo(feature) {
    const sigla = feature.properties.sigla;
    const info = ESTADOS[sigla];
    const cor = info && BIOMAS[info.bioma] ? BIOMAS[info.bioma].cor : "#9aa7b3";

    if (biomasReaisCarregados) {
      return { color: "#ffffff", weight: 1, opacity: 0.6, fillColor: cor, fillOpacity: 0 };
    }

    return {
      color: "#ffffff",
      weight: 1.2,
      fillColor: cor,
      fillOpacity: 0.75
    };
  }

  /* ----------------------------------------------------------
     5) Elementos do painel
     ---------------------------------------------------------- */
  const painelVazio   = document.getElementById("painelVazio");
  const painelConteudo = document.getElementById("painelConteudo");
  const biomaBadge    = document.getElementById("biomaBadge");
  const estadoNome    = document.getElementById("estadoNome");
  const plantaIcone   = document.getElementById("plantaIcone");
  const plantaNome    = document.getElementById("plantaNome");
  const plantaDesc    = document.getElementById("plantaDesc");
  const vegIcone      = document.getElementById("vegIcone");
  const vegNome       = document.getElementById("vegNome");
  const vegDesc       = document.getElementById("vegDesc");

  /* Cards clicáveis (levam à página de detalhes) */
  const cardPlanta    = document.getElementById("cardPlanta");
  const cardVegetacao = document.getElementById("cardVegetacao");

  let camadaAtiva = null;
  let estadoAtual = null; // guarda a sigla do estado selecionado

  /* ----------------------------------------------------------
     5.1) Abre a página de detalhes de um item
     ---------------------------------------------------------- */
  function abrirDetalhe(tipo) {
    if (!estadoAtual) return;
    const info = ESTADOS[estadoAtual];
    if (!info) return;

    const nome = tipo === "vegetacao" ? info.vegetacao : info.planta;
    const desc = tipo === "vegetacao" ? info.vegetacaoDesc : info.plantaDesc;

    const params = new URLSearchParams({
      tipo: tipo,
      nome: nome,
      estado: info.nome,
      bioma: info.bioma,
      desc: desc
    });

    window.location.href = "/detalhe?" + params.toString();
  }

  if (cardPlanta) {
    cardPlanta.addEventListener("click", function () { abrirDetalhe("planta"); });
    cardPlanta.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); abrirDetalhe("planta"); }
    });
  }

  if (cardVegetacao) {
    cardVegetacao.addEventListener("click", function () { abrirDetalhe("vegetacao"); });
    cardVegetacao.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); abrirDetalhe("vegetacao"); }
    });
  }

  /* ----------------------------------------------------------
     6) Preenche o painel lateral
     ---------------------------------------------------------- */
  function mostrarPainel(sigla) {
    const info = ESTADOS[sigla];
    if (!info) return;

    estadoAtual = sigla;

    painelVazio.style.display = "none";
    painelConteudo.style.display = "block";

    biomaBadge.textContent = info.bioma;
    biomaBadge.style.background =
      BIOMAS[info.bioma] ? BIOMAS[info.bioma].cor : "#18a999";

    estadoNome.textContent = info.nome;

    plantaIcone.textContent = info.plantaIcon;
    plantaNome.textContent = info.planta;
    plantaDesc.textContent = info.plantaDesc;

    vegIcone.textContent = info.vegetacaoIcon;
    vegNome.textContent = info.vegetacao;
    vegDesc.textContent = info.vegetacaoDesc;
  }

  /* ----------------------------------------------------------
     7) Interações por estado
     ---------------------------------------------------------- */
  function aoCriarFeature(feature, layer) {
    const sigla = feature.properties.sigla;
    const nome  = feature.properties.name;
    const info  = ESTADOS[sigla];

    layer.on({
      mouseover: function (e) {
        e.target.setStyle({ weight: 2.5, color: "#18a999", fillOpacity: 0.92 });
        e.target.bringToFront();
      },
      mouseout: function (e) {
        if (camadaAtiva) camadaAtiva.setStyle(estilo(camadaAtiva.feature));
        e.target.setStyle(estilo(feature));
      },
      click: function (e) {
        camadaAtiva = e.target;
        mostrarPainel(sigla);

        const popup = `
          <div class="popup-titulo">${nome} (${sigla})</div>
          <div class="popup-linha">🌿 <b>${info ? info.planta : "—"}</b></div>
          <div class="popup-linha">🌳 <b>${info ? info.vegetacao : "—"}</b></div>
          <div class="popup-linha">🌎 ${info ? info.bioma : "—"}</div>
        `;
        e.target.bindPopup(popup, { maxWidth: 260 }).openPopup();
      }
    });
  }

  /* ----------------------------------------------------------
     7.1) Escurece uma cor hex (para o contorno dos biomas)
     ---------------------------------------------------------- */
  function escurecer(hex, fator) {
    const num = parseInt(hex.replace("#", ""), 16);
    const r = Math.max(0, Math.floor(((num >> 16) & 255) * (1 - fator)));
    const g = Math.max(0, Math.floor(((num >> 8) & 255) * (1 - fator)));
    const b = Math.max(0, Math.floor((num & 255) * (1 - fator)));
    return `rgb(${r}, ${g}, ${b})`;
  }

  /* ----------------------------------------------------------
     7.2) Desenha um contorno único por região de bioma
     ----------------------------------------------------------
     Sem isso, o mapa só mostra 27 estados coloridos "soltos" e a
     divisão entre os biomas fica pouco perceptível. Aqui, com o
     Turf.js, os estados do mesmo bioma são "fundidos" (dissolve)
     e ganham um contorno grosso único por região — sem preencher
     por cima da cor de cada estado, e sem capturar cliques/hover
     (isso continua sendo feito pela camada de estados).
     ---------------------------------------------------------- */
  function desenharContornosDeBioma(geo) {
    if (typeof turf === "undefined") return; // Turf não carregou; segue sem o extra

    let regioes;
    try {
      // turf.dissolve só aceita Polygon (não MultiPolygon), então
      // "achatamos" cada estado em polígonos simples antes de fundir.
      const achatado = turf.flatten(geo);
      achatado.features.forEach(function (f) {
        f.properties.bioma = ESTADOS[f.properties.sigla]
          ? ESTADOS[f.properties.sigla].bioma
          : "Outro";
      });
      regioes = turf.dissolve(achatado, { propertyName: "bioma" });
    } catch (e) {
      console.warn("Não foi possível desenhar os contornos de bioma:", e);
      return;
    }

    L.geoJSON(regioes, {
      interactive: false, // deixa o hover/clique passar direto pros estados
      style: function (feature) {
        const bioma = feature.properties.bioma;
        const cor = BIOMAS[bioma] ? BIOMAS[bioma].cor : "#333";
        return {
          color: escurecer(cor, 0.35),
          weight: 3,
          opacity: 0.9,
          fill: false
        };
      }
    }).addTo(mapa);
  }

  /* ----------------------------------------------------------
     7.3) Limites REAIS dos biomas (fonte: IBGE)
     ----------------------------------------------------------
     Diferente do passo 7.2 (que só agrupa estados por bioma
     predominante), aqui usamos o contorno oficial dos 6 biomas
     do IBGE — o mesmo tipo de linha que aparece no mapa clássico
     de biomas do Brasil, cortando os estados ao meio quando é o
     caso (ex.: Bahia, Mato Grosso, Minas Gerais).

     O arquivo vem de dentro do próprio projeto (gerado uma vez a
     partir do shapefile oficial do IBGE, com mapshaper), então não
     depende de nenhum serviço externo nem de internet em produção.

     Se por algum motivo o arquivo não carregar (nome errado, não
     foi copiado etc.), o mapa cai de volta para a coloração por
     estado (função estilo() acima) e ainda desenha o contorno
     agrupado por bioma (passo 7.2), então nunca fica "quebrado".
     ---------------------------------------------------------- */
  function carregarBiomasReais(camadaEstados, geoEstados) {
    fetch("/static/data/br_biomas.json")
      .then(function (r) {
        if (!r.ok) throw new Error("HTTP " + r.status);
        return r.json();
      })
      .then(function (biomasGeo) {
        if (!biomasGeo || !Array.isArray(biomasGeo.features) || !biomasGeo.features.length) {
          throw new Error("Resposta sem feições de biomas");
        }

        L.geoJSON(biomasGeo, {
          interactive: false, // hover/clique continuam sendo dos estados, por cima
          style: function (feature) {
            const nomeBioma = feature.properties.Bioma;
            const cor = BIOMAS[nomeBioma] ? BIOMAS[nomeBioma].cor : "#9aa7b3";
            return {
              fillColor: cor,
              fillOpacity: 0.8,
              color: escurecer(cor, 0.3),
              weight: 1.5
            };
          }
        }).addTo(mapa);

        // Com o bioma real desenhado, os estados viram só contorno fino por cima
        biomasReaisCarregados = true;
        camadaEstados.setStyle(estilo);
      })
      .catch(function (err) {
        console.warn(
          "Não foi possível carregar os limites reais dos biomas (mantendo coloração por estado):",
          err
        );
        // Sem os limites reais, ao menos agrupa visualmente os estados por bioma
        desenharContornosDeBioma(geoEstados);
      });
  }

  /* ----------------------------------------------------------
     8) Carrega o GeoJSON dos estados
     ---------------------------------------------------------- */
  fetch("/static/data/br_estados.json")
    .then(function (r) { return r.json(); })
    .then(function (geo) {
      const camadaEstados = L.geoJSON(geo, {
        style: estilo,
        onEachFeature: aoCriarFeature
      }).addTo(mapa);

      carregarBiomasReais(camadaEstados, geo);
    })
    .catch(function (err) {
      console.error("Erro ao carregar o GeoJSON:", err);
      elMapa.innerHTML =
        '<p style="padding:20px;font-family:Arial">Não foi possível carregar o mapa.</p>';
    });

});