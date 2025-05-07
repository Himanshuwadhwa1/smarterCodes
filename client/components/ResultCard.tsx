"use client"
import { CircleChevronDown, CircleChevronUp, Code } from "lucide-react";
import { useState } from "react";

interface cardProps{
    content:string,
    score:number,
    url:string,
    html : string | undefined
}
export default function ResultCard({ content, score,url ,html} : cardProps) {
  const number = parseFloat(score.toFixed(2));
  const [show,setShow] = useState<boolean>(false);
  const handleClick = ()=>{
    setShow(yes => !yes)
  }
    return (
      <section className="border-dashed border-3 border-white p-1 mb-1 rounded-md">
        <div className="flex gap-4 justify-around p-2">
          <div dangerouslySetInnerHTML={{ __html: content }} className="w-250" />
          <p className="bg-green-200 w-fit h-fit text-black font-light p-1.5 rounded-sm"><strong>{number*100+50}%</strong> match </p>
        </div>
        <div className="m-2 px-4">
          <p>Path : {url}</p>
        </div>
        <div className="w-260 m-2 px-4">
          {html && (<h3 className="flex flex-col break-words overflow-x-auto whitespace-pre-wrap">
            <button className="cursor-pointer" onClick={handleClick}>
              <strong className="flex"><Code/> View HTML {show && <CircleChevronUp/>}{!show && <CircleChevronDown/>} :  </strong>
            </button>
            {show &&
             <p className="bg-[#252525] text-white self-center">
                {html}
            </p>}
            </h3>)}
          
        </div>
      </section>
    );
  }
  