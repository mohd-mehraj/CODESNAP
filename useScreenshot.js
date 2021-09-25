import download from "downloadjs";
import { toPng } from "html-to-image";
import React from "react";

/**
 * Hook to generate screenshot
 */
function useScreenshot() {
  const captureRef = React.useRef();

  const [status, setStatus] = React.useState("idle");

  async function generateImage(e) {
    e.preventDefault();
    if (!captureRef?.current) {
      return;
    }
    try {
      setStatus("loading");
      const imgBase64 = await toPng(captureRef.current, {
        quality: 1,
        pixelRatio: 1,
      });
      setStatus("success");
      download(imgBase64, "codeSnap.png");
    } catch (error) {
      setStatus("error");
      console.error(error);
    }
  }

  return {
    generateImage,
    captureRef,
    status,
  };
}

export default useScreenshot;
