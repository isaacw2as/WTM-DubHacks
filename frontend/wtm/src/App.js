import { useState } from "react";
import { createBrowserRouter, RouterProvider, Route, Navigate} from 'react-router-dom';
import SignUp from './Routes/SignUp';
import Login from './Routes/Login';
import Feed from './Routes/Feed';
import Event from './Routes/Event';
import CreatePost from './Routes/CreatePost';
import CreateEvent from './Routes/CreateEvent';


function App() {
  const [loggedInUser, setLoggedInUser] = useState("IsaacYun");

  const router = createBrowserRouter([
    {
      path: "/",
      element: <Login setLoggedInUser={setLoggedInUser} />
    },
    {
      path: "/signup",
      element: <SignUp setLoggedInUser={setLoggedInUser} />
    },
    {
      path: "/feed",
      element: loggedInUser !== null ? <Feed loggedInUser={loggedInUser} /> : <Navigate to={"/"} />
    },
    {
      path: "/createevent",
      element: loggedInUser !== null ? <CreateEvent loggedInUser={loggedInUser} /> : <Navigate to={"/"} />
    },
  ])

  return (
    <>
      <RouterProvider router={router} />
    </>
  );
}

export default App;
