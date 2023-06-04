import moment from "moment";

export function formatDateToString(date: Date | null): string {
    if (date === null) {
      return "";
    }
    return moment(date).format("YYYY-MM-DD");
  }