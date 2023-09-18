import React from "react";
import clsx from "clsx";
import ContentLoader from "react-content-loader";

interface MyLoaderProps {
  className?: string;
}

const MyLoader: React.FC<MyLoaderProps> = ({ className, ...props }) => {
  return (
    <div
      className={clsx(
        "flex flex-col items-center justify-center w-full h-full",
        className
      )}
      {...props}
    >

      <ContentLoader
        speed={1}
        width="100%" // Set width to 100% to fill the parent container
        height={115}
        viewBox="0 0 1180 115"
        backgroundColor="#deddda"
        foregroundColor="#ecebeb"
      >
        <rect x="0" y="11" rx="0" ry="0" width="227" height="42" />
        <rect x="141" y="103" rx="0" ry="0" width="1" height="0" />
        <rect x="1" y="78" rx="0" ry="0" width="222" height="40" />
        <rect x="255" y="33" rx="0" ry="0" width="218" height="5" />
        <rect x="369" y="87" rx="0" ry="0" width="84" height="30" />
        <circle cx="364" cy="37" r="9" />
      </ContentLoader>
    </div>
  );
};

export default MyLoader;
