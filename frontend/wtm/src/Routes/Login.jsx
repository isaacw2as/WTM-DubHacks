import React from 'react'
import { Link } from 'react-router-dom';
import '../Login.css';

export default function Login() {
  return (
    <>
      <div>
        <div className='loginhalf'>
          <div className='header'>Log in</div>
          <div>
            <input type='text' className='loginInput' name='username' placeholder='Username' maxLength={24}/>
          </div>
          <div>
            <input type='password' className='loginInput' name='password' placeholder='Password' maxLength={40}/>
          </div>
        </div>
        <div className='loginhalf'>
          <button className='loginbutton'>Log In</button>
          <div>Don't have an Account? <Link to='/signup' className='signup'>Sign Up</Link></div>
        </div>
        {/*Make sure I figure out if user signed up but didnt choose interests yet (closed page for example, login takes them to interests) */}
        {/*Make sure button changes color to my choice when hovered, then black when clicked*/}
      </div>
    </>
  )
}
