"use client"
import { FormEvent, useState } from 'react';
import axios from 'axios';
import ResultCard from '@/components/ResultCard';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Globe, Search } from 'lucide-react';
import { serverUrl } from '@/lib/env';

export default function Home() {
  const [url, setUrl] = useState<string>('');
  const [query, setQuery] = useState<string>('');
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [time,setTime] = useState();
  
  const handleSubmit = async (e : FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setResults([]);
    setTime(undefined);
    try {
      const body = {
        query,
        "website":url
      }
      const res = await axios.post(`${serverUrl}/search`, body);
      const data = await res.data;
      setResults(data.results);
      setTime(data.time)
    } catch (err) {
      console.error(err);
      alert('Error fetching results');
    }
    setLoading(false);
  };
  console.log(results);
  return (
    <div className='p-2 flex flex-col w-full h-full items-center my-8'>
      <h1 className='p-2 font-bold text-4xl'>Website content Search</h1>
      <p className='p-5'>Search through Website content with precision</p>
      <form onSubmit={handleSubmit} className='p-2 flex flex-col gap-2'>
        <div className='w-200 flex gap-1.5 items-center'>
        <Globe/>
        <Input placeholder='Enter Webiste URL' value={url} onChange={(e)=>setUrl(e.target.value)}  required />
        </div>
        <div className='flex gap-1.5 items-center'>
        <Search/>
        <Input placeholder='Enter your search query' value={query} onChange={(e)=>setQuery(e.target.value)} required />
        <Button type="submit" className='cursor-pointer' disabled={loading}>{loading ? 'Searching...' : 'Search'}</Button>
        </div>
      </form>

      <div className='mt-2 w-300 flex gap-2 flex-col'>
        {time && <p>Time taken to complete request is : {time}</p>}
        {results.map((chunk, i) => (
          <ResultCard key={i} content={chunk.content} score={chunk.score} url={chunk.url} html ={chunk?.html} />
        ))}
      </div>
    </div>
  );
}
