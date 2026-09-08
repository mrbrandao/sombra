import { defineConfig } from "vitepress";

export default defineConfig({
  title: "Sombra",
  description: "Local PII anonymization proxy for agent and LLM CLIs",
  base: "/sombra/",

  head: [
    ["link", { rel: "icon", href: "/sombra/img/favicon.ico" }],
  ],

  themeConfig: {
    logo: { src: "/img/sombra.png", alt: "Sombra", width: 32 },
    nav: [
      { text: "Getting Started", link: "/getting-started/install" },
      { text: "Concepts", link: "/concepts/architecture" },
      { text: "Reference", link: "/reference/make-targets" },
      { text: "Development", link: "/development/recognizers" },
    ],
    sidebar: [
      {
        text: "Getting Started",
        items: [
          { text: "Install", link: "/getting-started/install" },
          { text: "Configure OpenCode", link: "/getting-started/configure-opencode" },
          { text: "Use it", link: "/getting-started/use-it" },
        ],
      },
      {
        text: "Concepts",
        items: [
          { text: "Architecture", link: "/concepts/architecture" },
          { text: "What Sombra detects", link: "/concepts/what-sombra-detects" },
        ],
      },
      {
        text: "Reference",
        items: [
          { text: "Make targets", link: "/reference/make-targets" },
        ],
      },
      {
        text: "Development",
        items: [
          { text: "Recognizers", link: "/development/recognizers" },
          { text: "Adding an entity", link: "/development/adding-an-entity" },
          { text: "Testing", link: "/development/testing" },
          { text: "Quick tests", link: "/development/quick-tests" },
        ],
      },
    ],
    appearance: "dark",
    socialLinks: [],
    footer: {
      message: "Apache-2.0 · Sombra",
    },
  },
});