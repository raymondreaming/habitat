export type ChartMode = "volume" | "price" | "value" | "share" | "premium" | "risk";
export type AnalysisChartMode = Extract<ChartMode, "volume" | "price" | "value">;

export const CHART_MODES = [
  {
    id: "volume",
    label: "Volume",
    icon: "barChart",
    metricLabel: "Accepted MW",
    tooltip: "Analyze accepted cleared volume.",
  },
  {
    id: "price",
    label: "Price",
    icon: "trendingUp",
    metricLabel: "Average clearing price",
    tooltip: "Analyze average clearing price exposure.",
  },
  {
    id: "value",
    label: "Value",
    icon: "dollar",
    metricLabel: "Estimated gross value",
    tooltip: "Analyze estimated gross value contribution.",
  },
  {
    id: "share",
    label: "Share",
    icon: "percent",
    metricLabel: "Market share",
    tooltip: "Analyze Habitat share of accepted market volume.",
  },
  {
    id: "premium",
    label: "Premium",
    icon: "activity",
    metricLabel: "Price premium",
    tooltip: "Analyze Habitat price versus market average.",
  },
  {
    id: "risk",
    label: "Risk",
    icon: "shield",
    metricLabel: "Exceptions",
    tooltip: "Analyze negative-price exposure and concentration risks.",
  },
] as const;

export const ANALYSIS_CHART_MODES = CHART_MODES.filter((mode): mode is Extract<(typeof CHART_MODES)[number], { id: AnalysisChartMode }> =>
  mode.id === "volume" || mode.id === "price" || mode.id === "value",
);
