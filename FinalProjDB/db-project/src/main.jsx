import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import {createBrowserRouter, RouterProvider} from 'react-router-dom'
import './index.css'
import App from './App.jsx'
import CartPage from './CartPage.jsx'
import About from './About.jsx'  // ADD THIS LINE!

const router = createBrowserRouter([
{
  path: '/',
  element: <App/>
},
{
  path: '/orders',
  element: <Orders/>
},
{
  path: '/cart',
  element: <CartPage/>
},
{
  path: '/about',
  element: <About/>
},
]);

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <RouterProvider router = {router}/>
  </StrictMode>,
)
