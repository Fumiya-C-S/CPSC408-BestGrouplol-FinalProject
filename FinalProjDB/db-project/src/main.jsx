import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import {createBrowserRouter, RouterProvider} from 'react-router-dom'
import './index.css'
import App from './App.jsx'
import CartPage from './CartPage.jsx'

const router = createBrowserRouter([
{
  path: '/',
  element: <App/>
},
{
  path: '/cart',
  element: <CartPage/>
},
]);

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <RouterProvider router = {router}/>
    {/* <App /> */}
  </StrictMode>,
)
