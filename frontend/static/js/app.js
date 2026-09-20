/* ============================================================
   APP.JS — Utilitários globais do BioSistema
   ------------------------------------------------------------
   Expõe window.BioSistema com:
     - Sessao     : gerencia token/usuário no localStorage
     - API        : cliente HTTP central (token automático + 401)
     - toast()    : notificações flutuantes
     - Validacao  : validação de formulários
     - iniciarMenuMobile()
     - iniciarSessaoUI()
   Carregue este arquivo no base.html (antes dos scripts da página).
============================================================ */

(function () {
    "use strict";

    /* ========================================================
       SESSÃO — token e usuário no localStorage
    ======================================================== */

    const Sessao = {

        salvarToken(token) {
            localStorage.setItem("token", token);
        },

        obterToken() {
            return localStorage.getItem("token");
        },

        salvarUsuario(usuario) {
            localStorage.setItem("usuario", JSON.stringify(usuario));
        },

        obterUsuario() {
            try {
                return JSON.parse(localStorage.getItem("usuario"));
            } catch (e) {
                return null;
            }
        },

        estaLogado() {
            return Boolean(this.obterToken());
        },

        limpar() {
            localStorage.removeItem("token");
            localStorage.removeItem("usuario");
        },

        /* Redireciona para o login se não houver token */
        exigirLogin() {
            if (!this.estaLogado()) {
                window.location.href = "/login";
                return false;
            }
            return true;
        }
    };

    /* ========================================================
       API — cliente HTTP central
    ======================================================== */

    const API = {

        async requisitar(url, opcoes = {}) {

            const headers = Object.assign(
                { "Content-Type": "application/json" },
                opcoes.headers || {}
            );

            const token = Sessao.obterToken();

            if (token) {
                headers["Authorization"] = "Bearer " + token;
            }

            let resposta;

            try {
                resposta = await fetch(url, Object.assign({}, opcoes, { headers }));
            } catch (erro) {
                throw new Error("Não foi possível conectar ao servidor.");
            }

            /* Token expirado / inválido → volta ao login */
            if (resposta.status === 401) {
                Sessao.limpar();
                window.location.href = "/login";
                throw new Error("Sessão expirada. Faça login novamente.");
            }

            let dados = null;

            try {
                dados = await resposta.json();
            } catch (e) {
                dados = null;
            }

            if (!resposta.ok) {
                const mensagem =
                    (dados && (dados.erro || dados.mensagem)) ||
                    "Ocorreu um erro. Tente novamente.";
                throw new Error(mensagem);
            }

            return dados;
        },

        get(url)          { return this.requisitar(url); },
        post(url, corpo)  { return this.requisitar(url, { method: "POST",   body: JSON.stringify(corpo) }); },
        put(url, corpo)   { return this.requisitar(url, { method: "PUT",    body: JSON.stringify(corpo) }); },
        delete(url)       { return this.requisitar(url, { method: "DELETE" }); }
    };

    /* ========================================================
       TOAST — notificações flutuantes
    ======================================================== */

    function garantirContainerToast() {
        let container = document.querySelector(".toast-container");
        if (!container) {
            container = document.createElement("div");
            container.className = "toast-container";
            document.body.appendChild(container);
        }
        return container;
    }

    function toast(mensagem, tipo = "sucesso", duracao = 4000) {

        const icones = {
            sucesso: "✅",
            erro:    "⚠️",
            aviso:   "🔔"
        };

        const container = garantirContainerToast();

        const el = document.createElement("div");
        el.className = "toast toast-" + tipo;
        el.setAttribute("role", "status");

        el.innerHTML =
            '<span class="toast-icone">' + (icones[tipo] || "ℹ️") + "</span>" +
            '<span class="toast-texto"></span>';

        el.querySelector(".toast-texto").textContent = mensagem;

        container.appendChild(el);

        setTimeout(function () {
            el.classList.add("saindo");
            setTimeout(function () { el.remove(); }, 300);
        }, duracao);
    }

    /* ========================================================
       VALIDAÇÃO de formulários
    ======================================================== */

    const Validacao = {

        emailValido(email) {
            return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
        },

        senhaForte(senha) {
            return typeof senha === "string" && senha.length >= 8;
        },

        marcarErro(input, mensagem) {
            const grupo = input.closest(".input-group") || input.parentElement;
            grupo.classList.add("erro");

            let aviso = grupo.querySelector(".campo-erro");
            if (!aviso) {
                aviso = document.createElement("span");
                aviso.className = "campo-erro";
                grupo.appendChild(aviso);
            }
            aviso.textContent = mensagem;
        },

        limparErro(input) {
            const grupo = input.closest(".input-group") || input.parentElement;
            grupo.classList.remove("erro");
            const aviso = grupo.querySelector(".campo-erro");
            if (aviso) { aviso.remove(); }
        },

        limparTodos(form) {
            form.querySelectorAll(".input-group.erro").forEach(function (g) {
                g.classList.remove("erro");
            });
            form.querySelectorAll(".campo-erro").forEach(function (a) {
                a.remove();
            });
        }
    };

    /* ========================================================
       MENU MOBILE (hambúrguer)
    ======================================================== */

    function iniciarMenuMobile() {

        const toggle = document.getElementById("navToggle");
        const menu = document.getElementById("navMenu");

        if (!toggle || !menu) { return; }

        toggle.addEventListener("click", function () {
            const aberto = menu.classList.toggle("aberto");
            toggle.classList.toggle("ativo", aberto);
            toggle.setAttribute("aria-expanded", aberto ? "true" : "false");
        });

        /* Fecha o menu ao clicar em um link */
        menu.querySelectorAll("a").forEach(function (link) {
            link.addEventListener("click", function () {
                menu.classList.remove("aberto");
                toggle.classList.remove("ativo");
                toggle.setAttribute("aria-expanded", "false");
            });
        });
    }

    /* ========================================================
       UI DE SESSÃO — nome do usuário + logout
    ======================================================== */

    function iniciarSessaoUI() {

        const usuario = Sessao.obterUsuario();

        document.querySelectorAll("[data-nome-usuario]").forEach(function (el) {
            el.textContent = usuario ? usuario.nome : "Usuário";
        });

        document.querySelectorAll("[data-logout]").forEach(function (btn) {
            btn.addEventListener("click", async function () {
                try {
                    await API.post("/logout/", {});
                } catch (e) {
                    /* ignora erros de logout */
                } finally {
                    Sessao.limpar();
                    window.location.href = "/login";
                }
            });
        });
    }

    /* ========================================================
       EXPORTA
    ======================================================== */

    window.BioSistema = {
        Sessao: Sessao,
        API: API,
        toast: toast,
        Validacao: Validacao,
        iniciarMenuMobile: iniciarMenuMobile,
        iniciarSessaoUI: iniciarSessaoUI
    };

    /* Inicializa automaticamente o que é global */
    document.addEventListener("DOMContentLoaded", function () {
        iniciarMenuMobile();
        iniciarSessaoUI();
    });

})();
