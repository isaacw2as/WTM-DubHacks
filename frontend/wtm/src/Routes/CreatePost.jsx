import React, { useState } from 'react'
import axios from "axios"

const BACKEND_BASE_URL = "http://localhost:42069"
const UPLOAD_ENDPOINT = "/upload_files/upload"
const DOWNLOAD_ENDPOINT = "/upload_files/download"

export default function CreatePost({loggedInUser}) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [toDownload, setToDownload] = useState(null);
  const [downloadedFile, setDownloadedFile] = useState(null);

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0])
  }

  const handleUpload = async () => {
    if (!selectedFile) {
      return;
    }

    console.log("Attempt upload")
    console.log(selectedFile)

    const formData = new FormData()
    formData.append("file", selectedFile)

    try {
      const response = await axios.post(BACKEND_BASE_URL + UPLOAD_ENDPOINT, formData)
      console.log(response)

    } catch (error) {
      console.log("FUCK")
      console.log(error)
    }
  }

  const handleDownloadChange = (e) => {
    setToDownload(e.target.value)
  }

  const handleDownload = async () => {
    if (!toDownload) {
      return;
    }

    console.log("Attempt download")
    console.log(toDownload)

    try {
      const response = await axios.post(BACKEND_BASE_URL + DOWNLOAD_ENDPOINT, {filename: toDownload})
      console.log(response)

    } catch (error) {
      console.log("SHIT")
      console.log(error)
    }
  }

  const getSrc = (filename) => {
    const final = BACKEND_BASE_URL + DOWNLOAD_ENDPOINT + "?filename=" + filename
    console.log(final)
    return final
  }

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
            <input type='text' className='eventShortBox' name='day' placeholder='MM/DD/YYYY' maxLength={10}/>
            <input type='text' className='eventShortBox' name='starttime' placeholder='HH:MM' maxLength={5}/>
          </div>
          <div>
            <p className='eventParagraph'>Location</p>
            <input type='text' className='eventLongBox' name='location' placeholder='Where is your event happening?' maxLength={30}/>
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
  )
}