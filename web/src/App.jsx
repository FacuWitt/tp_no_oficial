import { createHashRouter, RouterProvider } from "react-router-dom";

import Layout from "./components/common/layout/Layout";
import Loader from "./components/common/loaders/Loader";
import Home from "./components/pages/Home";
import Shop from "./components/pages/Shop";

import { useState, useEffect } from "react";
import MercadoPagoSimulation from "./components/simulation/MercadoPagoSimulation";

const router = createHashRouter([
  {
    element: <Layout />,
    children: [
      { path: "/", element: <Home />, },
      { path: "/shop", element: <Shop />, },
      { path: "/mercadopago", element: <MercadoPagoSimulation />, },
    ]
  }
]);

const App = () => {
  const [loading, setLoading] = useState(false);

  // useEffect(() => {
  //   const timer = setTimeout(() => setLoading(false), 2000);
  //   return () => clearTimeout(timer);
  // }, []);

  return (
    <>
      {loading ? <Loader /> : <RouterProvider router={router} />}
    </>
  );
}

export default App;
