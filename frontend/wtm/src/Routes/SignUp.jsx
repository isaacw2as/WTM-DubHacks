import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import '../SignUp.css';

export default function SignUp({setLoggedInUser}) {
  return (
    <>
      <div>
        <div className='signupscreen'>
          <div className='signUpHeader'>Sign Up</div>
          <div>
            <input type='text' className='signUpInput' name='username' placeholder='Username' maxLength={24}/>
          </div>
          <div>
            <input type='password' className='signUpInput' name='password' placeholder='Password' maxLength={40}/>
          </div>
          <div>
              <p>Select up to 3 types of events you're interested in attending.</p>
          </div>
          <div className='buttonGrid'>
            <div>
                <button className='interestbutton'>Art</button>
                <button className='interestbutton'>Music</button>
                <button className='interestbutton'>Gaming</button>
            </div>
            <div>
                <button className='interestbutton'>Nature</button>
                <button className='interestbutton'>Culture</button>
                <button className='interestbutton'>Sports</button>
            </div>
            <div>
                <button className='interestbutton'>Fitness</button>
                <button className='interestbutton'>Travel</button>
                <button className='interestbutton'>Food</button>
            </div>
          </div>
          <button className='createAccount'>Create An Account</button>
          <div>Have an Account? <Link to='/' className='login'>Log In</Link></div>
        </div>
        {/* make button change color when clicked (button:click)*/}
      </div>
    </>
  )
}
