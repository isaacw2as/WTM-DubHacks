import { useState } from "react";
import { createBrowserRouter, RouterProvider, Route, Navigate} from 'react-router-dom';
import SignUp from './Routes/SignUp';
import Login from './Routes/Login';
import ChooseInterest from './Routes/ChooseInterest';
import Feed from './Routes/Feed';
import Event from './Routes/Event';
import CreatePost from './Routes/CreatePost';
import CreateEvent from './Routes/CreateEvent';


function App() {
  const [loggedInUser, setLoggedInUser] = useState("");

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
      path: "/chooseinterest",
      element: <ChooseInterest loggedInUser={loggedInUser} />
    },
    {
      path: "/feed",
      element: <Feed loggedInUser={loggedInUser} />
    },
    {
      path: "/createevent",
      element: <CreateEvent loggedInUser={loggedInUser} />
    },
    {
      path: "/createpost",
      element: <CreatePost loggedInUser={loggedInUser} />
    },
  ])

  return (
    <>
      <RouterProvider router={router} />
    </>
  );
}

export default App;
