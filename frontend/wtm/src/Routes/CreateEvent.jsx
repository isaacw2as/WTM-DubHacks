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
            <p className='eventParagraph'>Event Name</p>
            <input type='text' className='eventLongBox' name='username' placeholder='Name of Your Amazing Event ' maxLength={24}/>
          </div>
          <div>
            <p className='eventParagraph'>Time</p>
            <input type='text' className='eventShortBox' name='day' placeholder='DD/MM/YYYY' maxLength={10}/>
            <input type='text' className='eventShortBox' name='starttime' placeholder='HH:MM' maxLength={5}/>
            <input type='text' className='eventShortBox' name='endtime' placeholder='HH:MM' maxLength={5}/>
          </div>
          <div>
            <p className='eventParagraph'>Location</p>
            <input type='text' className='eventLongBox' name='location' placeholder='Where is your event happening?' maxLength={30}/>
          </div>
          <div className='onlineEvent'>
            <input type='checkbox' className='checkBox' name='password' placeholder='Password' maxLength={40}/>
            <p className='smallText'>My event is online.</p>
          </div>
          <div>
            <p className='eventParagraph'>Description</p>
            <input type='text' className='eventLongBox' name='description' placeholder={`Event description--what's the move?`} maxLength={30}/>
          </div>
          <div>
            <p className='eventParagraph'>Tags</p>
            <input type='text' className='eventLongBox' name='tags' placeholder='Type in keywords people can use to find your event.' maxLength={30}/>
          </div>
          <button className='createButton'>Create</button>
        </div>
      </div>
    </>
    // make button change color when clicked (button:click)
  )
}
