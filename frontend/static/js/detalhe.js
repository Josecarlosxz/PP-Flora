/* ============================================================
   DETALHE.JS — Página de detalhes (animal / vegetação)
   ------------------------------------------------------------
   Lê os parâmetros da URL (?tipo=animal&nome=Onça-pintada&...)
   e busca na Wikipédia (API pública, sem chave):
     - imagem real (originalimage / thumbnail)
     - resumo e texto detalhado (extract)
   Depende de: mapa_data.js (opcional, para o mapa de títulos)
============================================================ */

document.addEventListener("DOMContentLoaded", function () {

    /* ----------------------------------------------------------
       1) Lê os parâmetros da URL
    ---------------------------------------------------------- */
    const params = new URLSearchParams(window.location.search);

    const tipo    = params.get("tipo") || "planta";      // "planta" | "vegetacao"
    const nome    = params.get("nome") || "";
    const estado  = params.get("estado") || "";
    const bioma   = params.get("bioma") || "";
    const desc    = params.get("desc") || "";

    if (!nome) {
        mostrarErro("Nenhum item foi informado na URL.");
        return;
    }

    /* ----------------------------------------------------------
       2) Elementos da página
    ---------------------------------------------------------- */
    const elTipo        = document.getElementById("detalheTipo");
    const elNome        = document.getElementById("detalheNome");
    const elSub         = document.getElementById("detalheSub");
    const elImagem      = document.getElementById("detalheImagem");
    const elImgLoading  = document.getElementById("imagemLoading");
    const elCredito     = document.getElementById("detalheCredito");
    const elTxtLoading  = document.getElementById("textoLoading");
    const elTxtConteudo = document.getElementById("textoConteudo");
    const elResumo      = document.getElementById("detalheResumo");
    const elExtrato     = document.getElementById("detalheExtrato");
    const elHabitat     = document.getElementById("detalheHabitat");
    const elCurios      = document.getElementById("detalheCuriosidades");
    const elWiki        = document.getElementById("detalheWiki");
    const elErro        = document.getElementById("textoErro");
    const elErroDica    = document.getElementById("textoErroDica");

    /* ----------------------------------------------------------
       3) Cabeçalho imediato (não depende da rede)
    ---------------------------------------------------------- */
    const rotulo = tipo === "vegetacao" ? "Vegetação" : "Planta";
    elTipo.textContent = rotulo;
    elNome.textContent = nome;
    elSub.textContent  = [estado, bioma].filter(Boolean).join(" • ") || "Brasil";
    document.title = nome + " — BioSistema";

    /* ----------------------------------------------------------
       4) Descobre o título correto na Wikipédia
       Usa o mapa WIKI_TITULOS (de mapa_data.js) se existir;
       senão, usa o próprio nome.
    ---------------------------------------------------------- */
    let tituloWiki = nome;
    if (typeof WIKI_TITULOS !== "undefined" && WIKI_TITULOS[nome]) {
        tituloWiki = WIKI_TITULOS[nome];
    }

    const WIKI_API = "https://pt.wikipedia.org/w/api.php";

    /* ----------------------------------------------------------
       5) Busca o resumo + imagem (REST summary)
    ---------------------------------------------------------- */
    function buscarResumo() {
        const url = "https://pt.wikipedia.org/api/rest_v1/page/summary/" +
                    encodeURIComponent(tituloWiki);

        return fetch(url, { headers: { "Accept": "application/json" } })
            .then(function (r) {
                if (!r.ok) throw new Error("HTTP " + r.status);
                return r.json();
            });
    }

    /* ----------------------------------------------------------
       6) Busca o texto detalhado (Action API, extract completo)
    ---------------------------------------------------------- */
    function buscarTextoCompleto() {
        const url = WIKI_API +
            "?action=query&prop=extracts&explaintext=1&exintro=0" +
            "&redirects=1&format=json&origin=*&titles=" +
            encodeURIComponent(tituloWiki);

        return fetch(url)
            .then(function (r) { return r.json(); })
            .then(function (d) {
                const pages = d.query && d.query.pages;
                if (!pages) return "";
                const page = pages[Object.keys(pages)[0]];
                return (page && page.extract) ? page.extract : "";
            })
            .catch(function () { return ""; });
    }

    /* ----------------------------------------------------------
       7) Renderiza a imagem
    ---------------------------------------------------------- */
    function renderImagem(dados) {
        const img = (dados.originalimage && dados.originalimage.source) ||
                    (dados.thumbnail && dados.thumbnail.source);

        if (!img) {
            elImgLoading.innerHTML = "<p>🖼️ Imagem não disponível.</p>";
            return;
        }

        elImagem.onload = function () {
            elImgLoading.style.display = "none";
            elImagem.style.display = "block";
        };
        elImagem.onerror = function () {
            elImgLoading.innerHTML = "<p>🖼️ Não foi possível carregar a imagem.</p>";
        };
        elImagem.src = img;
        elImagem.alt = "Imagem de " + nome;

        if (dados.description) {
            elCredito.textContent = "Fonte: Wikipédia — " + dados.description;
        }
    }

    /* ----------------------------------------------------------
       8) Monta a seção "Onde vive"
    ---------------------------------------------------------- */
    function montarHabitat() {
        const partes = [];

        if (estado) {
            partes.push("No Brasil, este item está associado ao estado de " +
                        estado + ".");
        }
        if (bioma) {
            partes.push("Ocorre principalmente no bioma " + bioma + ".");
        }
        if (desc) {
            partes.push(desc);
        }
        if (!partes.length) {
            partes.push("Informações de distribuição não disponíveis.");
        }
        elHabitat.textContent = partes.join(" ");
    }

    /* ----------------------------------------------------------
       9) Monta "Curiosidades" a partir do texto da Wikipédia
    ---------------------------------------------------------- */
    function montarCuriosidades(texto) {
        elCurios.innerHTML = "";

        const itens = [];

        if (bioma)  itens.push("Bioma principal: " + bioma + ".");
        if (estado) itens.push("Estado destacado: " + estado + ".");

        // Pega frases curtas e informativas do texto
        if (texto) {
            const frases = texto
                .replace(/\s+/g, " ")
                .split(/(?<=[.!?])\s+/)
                .filter(function (f) { return f.length > 40 && f.length < 220; });

            frases.slice(0, 3).forEach(function (f) { itens.push(f.trim()); });
        }

        if (!itens.length) {
            elCurios.innerHTML = "<li>Sem curiosidades disponíveis.</li>";
            return;
        }

        itens.forEach(function (t) {
            const li = document.createElement("li");
            li.textContent = t;
            elCurios.appendChild(li);
        });
    }

    /* ----------------------------------------------------------
       10) Erro
    ---------------------------------------------------------- */
    function mostrarErro(msg) {
        if (elTxtLoading) elTxtLoading.style.display = "none";
        if (elTxtConteudo) elTxtConteudo.style.display = "none";
        if (elErro) {
            elErro.style.display = "block";
            elErroDica.textContent = msg || "";
        }
        if (elImgLoading) elImgLoading.innerHTML = "<p>🖼️ Indisponível.</p>";
    }

    /* ----------------------------------------------------------
       11) Executa
    ---------------------------------------------------------- */
    Promise.all([buscarResumo(), buscarTextoCompleto()])
        .then(function (resultados) {
            const resumo = resultados[0];
            const texto  = resultados[1];

            renderImagem(resumo);

            const extrato = resumo.extract || "";
            const longo   = texto || extrato;

            elResumo.textContent  = extrato || ("Informações sobre " + nome + ".");
            elExtrato.textContent = longo || "Texto detalhado não disponível.";

            montarHabitat();
            montarCuriosidades(longo);

            elWiki.href = "https://pt.wikipedia.org/wiki/" +
                          encodeURIComponent(tituloWiki);

            elTxtLoading.style.display = "none";
            elTxtConteudo.style.display = "block";
        })
        .catch(function (err) {
            console.error("Erro ao buscar dados:", err);
            mostrarErro("Verifique sua conexão com a internet e tente novamente.");
        });

});