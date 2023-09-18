import moment from "moment";

export function formatDateToString(date: Date | null): string {
  if (date === null) {
    return "";
  }
  return moment(date).format("YYYY-MM-DD");
}

export function formatToCelsius(data: number | string): string {
  if (typeof data === "number") {
    return `${data.toString()}°C`;
  }
  return `${data}°C`;
}
