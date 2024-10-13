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
      const response = axios.post(BACKEND_BASE_URL + DOWNLOAD_ENDPOINT, {filename: toDownload})
      console.log(response)

    } catch (error) {
      console.log("SHIT")
      console.log(error)
    }
  }

  return (
    <>
      <input type="file" onChange={handleFileChange}></input>
      <button onClick={handleUpload}>Upload File</button>
      <input type="text" onChange={handleDownloadChange} />
      <button onClick={handleDownload}>Download File</button>
      {
        downloadedFile ? 
        <image src={downloadedFile}></image> : <></>
      }
    </>
  )
}