import React from 'react';
import '../CreateEvent.css';

export default function CreateEvent({loggedInUser}) {
  return (
    <>
      <div className='eventpage'>
        <div className='Navbar'>

        </div>
        <div className='centerContent'>
          <div className='eventHeader'>Create Your Event</div>
          <div>
            <p>Event Name</p>
            <input type='text' className='eventInput' name='username' placeholder='Name of Your Amazing Event ' maxLength={24}/>
          </div>
          <div>
            <input type='password' className='eventInput' name='password' placeholder='Password' maxLength={40}/>
          </div>
          <div>
            <input type='checkbox' className='eventInput' name='password' placeholder='Password' maxLength={40}/>
          </div>
          <button className='createButton'>Create</button>
        </div>
      </div>
    </>
    // make button change color when clicked (button:click)
  )
}
