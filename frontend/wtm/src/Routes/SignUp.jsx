import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import '../SignUp.css';

export default function SignUp({setLoggedInUser}) {
  return (
    <>
      <div>
        <div className='signuphalf'>
          <div className='header'>Sign Up</div>
          <div>
            <input type='text' className='signUpInput' name='username' placeholder='Username' maxLength={24}/>
          </div>
          <div>
            <input type='password' className='signUpInput' name='password' placeholder='Password' maxLength={40}/>
          </div>
        </div>
        <div className='signuphalf'>
          <button className='createAccount'>Create An Account</button>
          <div>Have an Account? <Link to='/' className='login'>Log In</Link></div>
        </div>
      </div>
    </>
    // make button change color when clicked (button:click)
  )
}
