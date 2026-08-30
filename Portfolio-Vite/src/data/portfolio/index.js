import { themes } from "../../themes.js";
import { design } from "./design.js";
import { nav } from "./nav.js";
import { pages } from "./pages.js";
import { profile } from "./profile.js";
import { projects } from "./projects.js";
import { applyProjectPresentation } from "./presentation.js";

const presentedProjects = applyProjectPresentation(projects);

export const portfolioSchema = {
  profile,
  design,
  themes,
  nav,
  pages,
  projects: presentedProjects,
};
