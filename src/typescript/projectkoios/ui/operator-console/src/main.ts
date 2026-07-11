import "./styles.css";
import { OperatorConsoleApplicationFactory } from "./app";

const mountPoint: HTMLElement | null = document.querySelector("#app");

if (mountPoint === null) {
  throw new Error("Missing #app mount point");
}

mountPoint.innerHTML = new OperatorConsoleApplicationFactory().build().render();
