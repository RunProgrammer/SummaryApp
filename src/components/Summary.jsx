import React, { useState } from 'react';
import tSvg from '../assets/textSvg.svg';
import fSvg from '../assets/fileSvg.svg';
import lSvg from '../assets/linkSvg.svg';
import uSvg from '../assets/uploadSvg.svg';
import axios from 'axios';

function Summary() {
  const [textBox, setTextbox] = useState(false);
  const [urlBox, setUrlbox] = useState(false);
  const [fileBox, setFilebox] = useState(false);
  
  // Handling the input
  const [inputText, setInputText] = useState('');
  const [inputUrl, setInputUrl] = useState('');
  const [inputFile,setInputFile] = useState('')
  const [summary, setSummary] = useState('');
  
  const [getTextsum,setTextsum] = useState('')

  // Function that handles text input change
  const handleText = (e) => {
    setInputText(e.target.value);
  };

  const handleUrl = (e) => {
    setInputUrl(e.target.value);
  };

  const handleFile = (e) => {
    const fileName = e.target.files[0];
    setInputFile(fileName);
  };

  // Summarize text from input
  const summarizeText = async () => {
    try {
      const response = await axios.post('http://localhost:5000/summary/text', { text: inputText });
      const finalResponse = response.data.summary
      setSummary(finalResponse);
      setTextsum(finalResponse)
    } catch (error) {
      console.error('Error summarizing text:', error);
      setSummary('An error occurred while summarizing the text.');
    }
  };

  // Summarize text from YouTube URL
  const summarizeLink = async () => {
    console.log('Sending URL:', inputUrl); // Debugging log
    try {
      const response = await axios.post('http://localhost:5000/summary/youtube', { video_url: inputUrl });
      console.log('Response:', response.data); // Debugging log
      setSummary(response.data.summary);
    } catch (error) {
      console.error('Error summarizing YouTube link:', error.response ? error.response.data : error.message);
      setSummary('An error occurred while summarizing the YouTube link.');
    }
  };

    // Handle file summarization
    const summarizeFile = async () => {
      const formData = new FormData();
      formData.append('file', inputFile);
  
      try {
        const response = await axios.post('http://localhost:5000/summary/file', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        const finalResponse = response.data.summary;
        setSummary(finalResponse);
      } catch (error) {
        console.error('Error summarizing file:', error);
        setSummary('An error occurred while summarizing the file.');
      }
    };

  const summarizeCombined = async () => {
    if (inputText && inputUrl) {
      try {
        const response = await axios.post('http://localhost:5000/summary/combined', {
          text: inputText,
          video_url: inputUrl,
          
        });

        const finalResponse = response.data.summary;
        setSummary(finalResponse);
      } catch (error) {
        console.error('Error summarizing combined content:', error);
        setSummary('An error occurred while summarizing the combined content.');
      }
    } else if (textBox && inputText && urlBox && inputUrl && fileBox && inputFile){
      try {
        const response = await axios.post('http://localhost:5000/summary/all',{
          text : inputText,
          video_url : inputUrl,
          file : inputFile  

        })
        const finalResponse = response.data.summary;
        setSummary(finalResponse);

      } catch (error) {
        console.error('Error summarizing combined content:', error);
        setSummary('An error occurred while summarizing the combined content.');
      }
      
      
    }
     else {
      setSummary('Please provide both text and a YouTube URL to combine.');
    }
  };

  const summTotal = async () => {
    if (textBox && inputText && urlBox && inputUrl && fileBox && inputFile) {
      // If both text and URL are provided, combine them
      summarizeCombined();
    } else if (textBox && inputText) {
      // If only text is provided
      summarizeText();
    } else if (urlBox && inputUrl) {
      // If only URL is provided
      summarizeLink();
    } else if (fileBox && inputFile){
      summarizeFile()
    } else {
      setSummary('Please enter text or a URL to summarize.');
    }
  };
  

  return (
    <div className="bg-gray-900 w-full h-screen duration-300 relative">
      <div className="flex justify-center p-4">
        <h1 className="text-[40px] text-emerald-200 underline font-mono font-semibold">Any Summary</h1>
      </div>
      <div className="flex-row">
        <div className="flex flex-col mt-28">
          <div className="bg-slate-900 border-2 shadow-2xl border-slate-600 max-w-[60px] rounded-r-2xl min-h-[250px] flex justify-center items-center">
            <div className="flex-col text-2xl font-sans font-normal ">
              <p onClick={() => {setTextbox(!textBox)}}>
                <img src={tSvg} alt="" className="max-w-[35px] cursor-pointer duration-100 hover:border-2 border-[#e879f9]"/>
              </p>
              <p onClick={() => {setFilebox(!fileBox)}}>
                <img src={fSvg} alt="" className="max-w-[35px] cursor-pointer mt-7 duration-100 hover:border-2 border-violet-400"/>
              </p>
              <p onClick={() => {setUrlbox(!urlBox) }}>
                <img src={lSvg} alt="" className="max-w-[35px] cursor-pointer mt-7 duration-100 hover:border-2 border-cyan-300"/>
              </p>
              <p onClick={summTotal}>
                <img src={uSvg} alt="" className="max-w-[35px] cursor-pointer mt-7 duration-100 hover:border-2 border-red-400"/>
              </p>
            </div>
          </div>
        </div>
      </div>
      <div className="absolute top-1/2 sm:m-2 sm:left-[250px] left-[220px] transform -translate-x-1/2 -translate-y-1/2">
        <div className="flex-col p-2">
          <div id="textDiv" className="max-h-[300px] bg-slate-800 p-4 shadow-2xl rounded-2xl sm:mt-4 max-w-[300px] duration-500" style={{display: textBox ? 'block' : 'none'}}>
            <h2 className="text-pink-400 text-xl font-sans font-semibold">Text</h2>
            <textarea name="textInput" value={inputText} onChange={handleText} className="bg-white transition-shadow duration-700 border-4 text-pink-900 text-lg font-semibold font-mono border-pink-300 rounded-2xl mt-2 p-1 min-h-[150px] max-w-[300px] outline-none"/>
          </div>
          {/* TODO: File */}
          <div id="fileDiv" className="max-h-[300px] mt-8 bg-slate-800 pb-8 py-2 px-6 shadow-2xl rounded-2xl max-w-[300px] duration-500" style={{display: fileBox ? 'block' : 'none'}}>
            <h2 className="text-purple-400 text-xl font-sans font-semibold mb-4">File</h2>
            <input type="file" id="fileInput" onChange={handleFile} className="hidden"/> 
            <label htmlFor="fileInput" className="text-purple-400 px-4 border-4 border-purple-300 rounded-2xl py-2 bg-white text-xl font-sans font-semibold cursor-pointer duration-300 hover:bg-slate-950 hover:text-white">Choose File</label>
          </div>
          
          {/* TODO: Link */}
          <div id="linkDiv" className="max-h-[300px] bg-slate-800 p-4 shadow-2xl rounded-2xl mt-16 max-w-[300px] duration-500" style={{display: urlBox ? 'block' : 'none'}}>
            <h2 className="text-cyan-400 text-xl font-sans font-semibold">Link</h2>
            <input type="text" name="urlInput" value={inputUrl} onChange={handleUrl} className="bg-white border-4 text-cyan-900 text-lg font-semibold font-mono border-cyan-300 rounded-2xl mt-2 p-1 outline-none"/>
          </div>
        </div>
      </div>
      <div className="bg-slate-800 font-semibold flex justify-center rounded-2xl sm:min-h-[500px] sm:max-w-[700px] h-[400px] w-full absolute sm:top-1/2 top-[900px] sm:m-10 mt-20 sm:left-[850px] left-[50%] transform -translate-x-1/2 -translate-y-1/2">
        <div className="flex-col text-center">
          <h1 className="sm:text-[30px] text-xl text-amber-200 mt-2">Result</h1>
          <textarea
            name="Resultop"
            id="rOP"
            value={summary}
            readOnly
            className="min-h-[320px] bg-slate-900 overflow-y-auto shadow-2xl scroll-smooth p-2 sm:text-lg font-semibold font-mono text-amber-500 max-h-[320px] min-w-[350px] max-w-[350px] sm:min-w-[650px] rounded-xl sm:min-h-[420px] mt-4 sm:max-h-[350px] outline-none"
          />
        </div>
      </div>
    </div>
  );
}

export default Summary;
