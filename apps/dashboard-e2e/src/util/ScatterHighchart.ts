// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

import { Chart, IChartElement } from "./Chart";

const dReg = /^M ([\d.]+) ([\d.]+) A 3 3 0 1 1 ([\d.]+) ([\d.]+) Z$/;
const qReg =
  /^M ([\d.]+) ([\d.]+) L ([\d.]+) ([\d.]+) L ([\d.]+) ([\d.]+) L ([\d.]+) ([\d.]+) Z$/; //quadrangle coordinates

export interface IHighScatter extends IChartElement {
  readonly x?: number;
  readonly y1?: number;
  readonly y2?: number;
  readonly y3?: number;
}
export class ScatterHighchart extends Chart<IHighScatter> {
  public get Elements(): IHighScatter[] {
    return this.getHighChartHtmlElements("path").map((b, i) =>
      this.getCoordinate(b, i)
    );
  }

  public sortByH(): IHighScatter[] {
    return this.Elements.sort((a, b) => a.top - b.top);
  }
  public clickNthPoint(idx: number): void {
    const offset = this.getNthPointOffset(idx);
    if (!offset) {
      return;
    }
    cy.get(`${this.container} .nsewdrag.drag`).trigger("mousedown", {
      clientX: offset.left,
      clientY: offset.top,
      eventConstructor: "MouseEvent",
      force: true
    });
    cy.document().then((doc) => {
      const event = new MouseEvent("mouseup", {
        bubbles: true,
        clientX: offset.left,
        clientY: offset.top
      });
      doc.dispatchEvent(event);
    });
  }

  private getNthPointOffset(idx: number): JQuery.Coordinates | undefined {
    return cy.$$(`.trace.scatter:eq(0) .points path:eq(${idx})`).offset();
  }

  private readonly getCoordinate = (
    element: HTMLElement,
    idx: number
  ): IHighScatter => {
    const d = element.getAttribute("d");
    if (!d) {
      throw new Error(
        `${idx}th path element in svg does not have "d" attribute`
      );
    }
    const exec = dReg.exec(d);
    if (!exec) {
      const qExec = qReg.exec(d);
      if (qExec) {
        const [, ...strCords] = qExec;
        const [x1, y1, x2, y2, x3, y3, x4, y4] = strCords.map((s) => Number(s));
        return {
          bottom: x2,
          left: x4,
          right: x3,
          top: y4,
          x: x1,
          y1,
          y2,
          y3
        };
      }
      throw new Error(
        `${idx}th path element in svg have invalid "d" attribute`
      );
    }
    const [, ...strCords] = exec;
    const [x, y1, horTip, vertTip, yChange, height] = strCords.map((s) =>
      Number(s)
    );
    if (horTip === vertTip) {
      throw new Error("Horizontal tip is equal to vertical length");
    }
    return {
      bottom: x, // x
      left: y1, // y1
      right: yChange, // y2
      top: height // y3
    };
  };
}
