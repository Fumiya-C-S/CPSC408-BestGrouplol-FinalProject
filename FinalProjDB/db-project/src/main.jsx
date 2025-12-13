import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import {createBrowserRouter, RouterProvider} from 'react-router-dom'
import './index.css'
import App from './App.jsx'
import CartPage from './CartPage.jsx'
import About from './About.jsx'
import Orders from './Orders.jsx'

//Creates a brower router instance with specified paths. 
const router = createBrowserRouter([
{
  path: '/', //Homepage is our App.jsx
  element: <App/>
},
{
  path: '/orders', //Orders page is our Orders.jsx
  element: <Orders/>
},
{
  path: '/cart', //Cart is our CartPage.jsx
  element: <CartPage/>
},
{
  path: '/about', //About page is our About.jsx
  element: <About/>
},
]);

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <RouterProvider router = {router}/>
  </StrictMode>,
)
