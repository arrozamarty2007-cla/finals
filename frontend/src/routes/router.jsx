import { createBrowserRouter, Navigate } from 'react-router-dom';
import App from '../App';
import Shop from '../pages/Shop';
import Cart from '../pages/Cart';
import Orders from '../pages/Orders';

export const routes = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      { index: true, element: <Navigate to="/shop" replace /> },
      { path: 'shop', element: <Shop /> },
      { path: 'cart', element: <Cart /> },
      { path: 'orders', element: <Orders /> },
    ],
  },
]);
