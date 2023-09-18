import React from "react";
import LoadingSpinner from "./LoadingSpinner";

interface ButtonProps {
  text: string;
  icon?: React.ReactElement;
  disabled?: boolean;
  onClick: () => void;
  isLoading?: boolean;
}

const Button: React.FC<ButtonProps> = ({
  text,
  icon,
  disabled,
  onClick,
  isLoading,
}) => {
  return (
    <button
      type="button"
      className={`flex items-center bg-blue-500 hover:bg-blue-600 text-white text-lg font-medium rounded-md ${
        disabled || isLoading ? "opacity-50 cursor-not-allowed" : ""
      }`}
      onClick={disabled || isLoading ? undefined : onClick}
      disabled={disabled || isLoading}
    >
      <span className="ml-2 mr-2">{text}</span>
      {icon && !isLoading && (
        <span style={{ width: 24, height: 24 }}>{icon}</span>
      )}
      {isLoading && <LoadingSpinner />}
    </button>
  );
};

export default Button;
