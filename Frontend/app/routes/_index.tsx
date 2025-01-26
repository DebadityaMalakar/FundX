import type { MetaFunction } from "@remix-run/node";
import Navbar from "~/components/Navbar";

export const meta: MetaFunction = () => {
  return [
    { title: "Home" },
    { name: "description", content: "Welcome to FundX" },
  ];
};

export default function Index() {
  return (
    <div className="bg-black text-white h-screen">
      <Navbar/>
      <div className="h-4/5 flex justify-center items-center">
       <p className="text-bold text-4xl">
        Business Redefined
       </p>
      </div>
    </div>
  );
}
