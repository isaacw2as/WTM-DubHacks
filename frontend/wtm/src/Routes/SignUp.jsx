import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { CREATE_USER_ENDPOINT } from '../endpoints';
import '../SignUp.css';
import axios from "axios"

export default function SignUp({setLoggedInUser}) {
  const [username, setUsername] = useState(null);
  const [password, setPassword] = useState(null);
  const [selectedInterests, setSelectedInterests] = useState([]);
  const nav = useNavigate()

  const onChangeUsername = (e) => {
    setUsername(e.target.value)
  }

  const onChangePassword = (e) => {
    setPassword(e.target.value)
  }

  const onClickArt = (e) => {
    const newInterests = [...selectedInterests]
    if (selectedInterests.includes("art")) {
      const idx = newInterests.indexOf("art");
      newInterests.splice(idx, 1);
      e.target.classList.remove("interestbutton-selected")
      e.target.classList.add("interestbutton")
    } else if (newInterests.length < 3) {
      newInterests.push("art")
      e.target.classList.remove("interestbutton")
      e.target.classList.add("interestbutton-selected")
    }

    setSelectedInterests(newInterests)
  }

  const onClickMusic = (e) => {
    const newInterests = [...selectedInterests]
    if (newInterests.includes("music")) {
      const idx = newInterests.indexOf("music");
      newInterests.splice(idx, 1);
      e.target.classList.remove("interestbutton-selected")
      e.target.classList.add("interestbutton")
    } else if (newInterests.length < 3) {
      newInterests.push("music")
      e.target.classList.remove("interestbutton")
      e.target.classList.add("interestbutton-selected")
    }

    setSelectedInterests(newInterests)
  }

  const onClickGaming = (e) => {
    const newInterests = [...selectedInterests]
    if (newInterests.includes("gaming")) {
      const idx = newInterests.indexOf("gaming");
      newInterests.splice(idx, 1);
      e.target.classList.remove("interestbutton-selected")
      e.target.classList.add("interestbutton")
    } else if (newInterests.length < 3) {
      newInterests.push("gaming")
      e.target.classList.remove("interestbutton")
      e.target.classList.add("interestbutton-selected")
    }

    setSelectedInterests(newInterests)
  }

  const onClickNature = (e) => {
    const newInterests = [...selectedInterests]
    if (newInterests.includes("nature")) {
      const idx = newInterests.indexOf("nature");
      newInterests.splice(idx, 1);
      e.target.classList.remove("interestbutton-selected")
      e.target.classList.add("interestbutton")
    } else if (newInterests.length < 3) {
      newInterests.push("nature")
      e.target.classList.remove("interestbutton")
      e.target.classList.add("interestbutton-selected")
    }

    setSelectedInterests(newInterests)
  }

  const onClickCulture = (e) => {
    const newInterests = [...selectedInterests]
    if (newInterests.includes("culture")) {
      const idx = newInterests.indexOf("culture");
      newInterests.splice(idx, 1);
      e.target.classList.remove("interestbutton-selected")
      e.target.classList.add("interestbutton")
    } else if (newInterests.length < 3) {
      newInterests.push("culture")
      e.target.classList.remove("interestbutton")
      e.target.classList.add("interestbutton-selected")
    }

    setSelectedInterests(newInterests)
  }

  const onClickSports = (e) => {
    const newInterests = [...selectedInterests]
    if (newInterests.includes("sports")) {
      const idx = newInterests.indexOf("sports");
      newInterests.splice(idx, 1);
      e.target.classList.remove("interestbutton-selected")
      e.target.classList.add("interestbutton")
    } else if (newInterests.length < 3) {
      newInterests.push("sports")
      e.target.classList.remove("interestbutton")
      e.target.classList.add("interestbutton-selected")
    }

    setSelectedInterests(newInterests)
  }

  const onClickFitness = (e) => {
    const newInterests = [...selectedInterests]
    if (newInterests.includes("fitness")) {
      const idx = newInterests.indexOf("fitness");
      newInterests.splice(idx, 1);
      e.target.classList.remove("interestbutton-selected")
      e.target.classList.add("interestbutton")
    } else if (newInterests.length < 3) {
      newInterests.push("fitness")
      e.target.classList.remove("interestbutton")
      e.target.classList.add("interestbutton-selected")
    }

    setSelectedInterests(newInterests)
  }

  const onClickTravel = (e) => {
    const newInterests = [...selectedInterests]
    if (newInterests.includes("travel")) {
      const idx = newInterests.indexOf("travel");
      newInterests.splice(idx, 1);
      e.target.classList.remove("interestbutton-selected")
      e.target.classList.add("interestbutton")
    } else if (newInterests.length < 3) {
      newInterests.push("travel")
      e.target.classList.remove("interestbutton")
      e.target.classList.add("interestbutton-selected")
    }

    setSelectedInterests(newInterests)
  }

  const onClickFood = (e) => {
    const newInterests = [...selectedInterests]
    if (newInterests.includes("food")) {
      const idx = newInterests.indexOf("food");
      newInterests.splice(idx, 1);
      e.target.classList.remove("interestbutton-selected")
      e.target.classList.add("interestbutton")
    } else if (newInterests.length < 3) {
      newInterests.push("food")
      e.target.classList.remove("interestbutton")
      e.target.classList.add("interestbutton-selected")
    }

    setSelectedInterests(newInterests)
  }

  const submitSignUp = async (e) => {
    if (username && password && selectedInterests.length > 0) {
      axios.post(CREATE_USER_ENDPOINT, { username: username, password: password, interests: selectedInterests})
      .then(() => {
        setLoggedInUser(username)
        nav("/feed")
      }).catch((error) => {
        console.log("Unable to create user")
      })
    }
  }

  return (
    <>
      <div className='signupscreen'>
        <div className='signUpHeader'>Sign Up</div>
        <div>
          <input type='text' className='signUpInput' name='username' placeholder='Username' maxLength={24} onChange={onChangeUsername}/>
        </div>
        <div>
          <input type='password' className='signUpInput' name='password' placeholder='Password' maxLength={40} onChange={onChangePassword}/>
        </div>
        <div>
            <p>Select up to 3 types of events you're interested in attending.</p>
        </div>
        <div className='buttonGrid'>
          <div>
              <button className='interestbutton' onClick={onClickArt}>Art</button>
              <button className='interestbutton' onClick={onClickMusic}>Music</button>
              <button className='interestbutton' onClick={onClickGaming}>Gaming</button>
          </div>
          <div>
              <button className='interestbutton' onClick={onClickNature}>Nature</button>
              <button className='interestbutton' onClick={onClickCulture}>Culture</button>
              <button className='interestbutton' onClick={onClickSports}>Sports</button>
          </div>
          <div>
              <button className='interestbutton' onClick={onClickFitness}>Fitness</button>
              <button className='interestbutton' onClick={onClickTravel}>Travel</button>
              <button className='interestbutton' onClick={onClickFood}>Food</button>
          </div>
        </div>
        <button className='createAccount' onClick={submitSignUp}>Create An Account</button>
        <div>Have an Account? <Link to='/' className='login'>Log In</Link></div>
      </div>
      {/* make button change color when clicked (button:click)*/}
    </>
  )
}
