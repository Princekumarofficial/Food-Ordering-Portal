"use client";

import React from "react";
import { useRouter } from "next/navigation";

const OrderConfirmationPage = () => {
  const router = useRouter();

  const handleReturnHome = () => {
    router.push("/");
  };

  return (
    <div className="container p-8 justify-center items-center flex flex-col">
      <h1 className="font-semibold text-2xl my-2">Order Confirmed!</h1>
      <p className="text-center p-4 ">
        Thank you for your purchase. Your order has been successfully placed.
      </p>
      <button
        onClick={handleReturnHome}
        style={{
          padding: "10px 20px",
          fontSize: "16px",
          backgroundColor: "#4CAF50",
          color: "white",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer",
        }}
        className="my-4"
      >
        Return to Home
      </button>
    </div>
  );
};

export default OrderConfirmationPage;
