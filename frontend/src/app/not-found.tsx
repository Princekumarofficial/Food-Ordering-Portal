import { AlertTriangle, Pizza, Coffee, IceCream } from "lucide-react";
import { Button } from "@/components/ui/button";
import Link from "next/link";

const ErrorPage = ({ message = "Oops! Something went wrong." }) => {
  return (
    <div className="fixed inset-0 bg-orange-50 flex flex-col items-center justify-center z-50">
      <div className="text-center max-w-md px-4">
        <div className="mb-8 relative flex flex-col gap-4">
          <AlertTriangle className="w-24 h-24 text-orange-500 mx-auto" />
          <div className="flex justify-center items-center">
            <div className="animate-bounce">
              <Pizza className="w-8 h-8 text-orange-600" />
            </div>
            <div className="animate-bounce" style={{ animationDelay: "0.2s" }}>
              <Coffee className="w-8 h-8 text-orange-600" />
            </div>
            <div className="animate-bounce" style={{ animationDelay: "0.4s" }}>
              <IceCream className="w-8 h-8 text-orange-600" />
            </div>
          </div>
        </div>
        <h2 className="text-3xl font-bold text-orange-600 mb-4">
          Oops! We dropped the plate
        </h2>
        <p className="text-orange-800 mb-8">{message}</p>
        <Link href="/">
          <Button className="bg-orange-500 hover:bg-orange-600">
            Return to Home Menu
          </Button>
        </Link>
      </div>
    </div>
  );
};

export default ErrorPage;
