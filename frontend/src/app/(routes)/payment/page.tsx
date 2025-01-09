"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { get_cart } from "@/helpers/api";

interface CartItem {
  id: number;
  name: string;
  price: number;
  quantity: number;
}

export default function CheckoutPage() {
  const router = useRouter();
  const [step, setStep] = useState("address");

  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const [address, setAddress] = useState({
    street: "",
    city: "",
    state: "",
    zipCode: "",
  });

  const handleAddressChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setAddress({ ...address, [e.target.name]: e.target.value });
  };

  const handleAddressSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setStep("payment");
  };

  const handlePaymentSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Here you would typically process the order
    // For now, we'll just redirect to a confirmation page
    router.push("/order-confirmation");
  };

  const totalPrice = cartItems.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  );

  useEffect(() => {
    get_cart().then((data) => {
      const tempData = data.items.map((item: any) => ({
        id: item.id,
        name: item.food_item.name,
        price: item.food_item.price,
        quantity: item.quantity,
      }));
      setCartItems(tempData);
    });
  }, []);

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-orange-600 mb-6">Checkout</h1>
      {step === "address" ? (
        <Card>
          <CardHeader>
            <CardTitle>Delivery Address</CardTitle>
            <CardDescription>
              Please enter your delivery address
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleAddressSubmit}>
              <div className="grid gap-4">
                <div>
                  <Label htmlFor="street">Street Address</Label>
                  <Input
                    id="street"
                    name="street"
                    value={address.street}
                    onChange={handleAddressChange}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="city">City</Label>
                  <Input
                    id="city"
                    name="city"
                    value={address.city}
                    onChange={handleAddressChange}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="state">State</Label>
                  <Input
                    id="state"
                    name="state"
                    value={address.state}
                    onChange={handleAddressChange}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="zipCode">ZIP Code</Label>
                  <Input
                    id="zipCode"
                    name="zipCode"
                    value={address.zipCode}
                    onChange={handleAddressChange}
                    required
                  />
                </div>
              </div>
              <Button
                type="submit"
                className="mt-4 bg-orange-500 hover:bg-orange-600"
              >
                Continue to Payment
              </Button>
            </form>
          </CardContent>
        </Card>
      ) : (
        <Card>
          <CardHeader>
            <CardTitle>Payment</CardTitle>
            <CardDescription>Please select your payment method</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handlePaymentSubmit}>
              <RadioGroup defaultValue="cod">
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="cod" id="cod" />
                  <Label htmlFor="cod">Cash on Delivery</Label>
                </div>
              </RadioGroup>
              <div className="mt-6">
                <h3 className="font-semibold mb-2">Order Summary</h3>
                {cartItems.map((item) => (
                  <div key={item.id} className="flex justify-between mb-2">
                    <span>
                      {item.name} x {item.quantity}
                    </span>
                    <span>Rs. {(item.price * item.quantity).toFixed(2)}</span>
                  </div>
                ))}
                <div className="flex justify-between font-bold mt-2">
                  <span>Total</span>
                  <span>Rs. {totalPrice.toFixed(2)}</span>
                </div>
              </div>
              <div className="mt-4">
                <h3 className="font-semibold mb-2">Delivery Address</h3>
                <p>{address.street}</p>
                <p>
                  {address.city}, {address.state} {address.zipCode}
                </p>
              </div>
              <Button
                type="submit"
                className="mt-4 bg-orange-500 hover:bg-orange-600"
              >
                Place Order
              </Button>
            </form>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
