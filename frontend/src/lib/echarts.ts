import { BarChart } from "echarts/charts";
import { GridComponent, LegendComponent, TooltipComponent } from "echarts/components";
import { init, use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import type { EChartsOption } from "echarts";

use([BarChart, GridComponent, LegendComponent, TooltipComponent, CanvasRenderer]);

export { init };
export type { EChartsOption };
