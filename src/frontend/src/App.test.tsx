import React from "react";
import { render, screen } from "@testing-library/react";
import App from "./App";

describe("App", () => {
  it("renders the title", () => {
    render(<App />);
    const titleElement = screen.getByText(/Solar and AC data/i);
    expect(titleElement).toBeInTheDocument();
  });

  // Add more test cases for other functionality
});
