import React, { useEffect, useState } from 'react';
import BookSlicer from './BookSlicer';
import { MdChevronLeft, MdChevronRight } from 'react-icons/md';


export default function Row({title, list, rowID }) {
    
  const [projects, setProjects] = useState([]);
  console.log("SIEMA", projects)
  console.log(rowID)
  useEffect(() => {
    setProjects(list);
  }, [list]);

  const slideLeft = () => {
    var slider = document.getElementById('slider' + rowID);
    slider.scrollLeft = slider.scrollLeft - 500;
  };

  const slideRight = () => {
    var slider = document.getElementById('slider' + rowID);
    slider.scrollLeft = slider.scrollLeft + 500;
  };


  return (
    <>
      <h2 className='text-white font-bold md:text-4xl p-4'>{title}</h2>
      <div className='relative flex items-center group'>
        <MdChevronLeft
          onClick={slideLeft}
          className='bg-white left-0 rounded-full absolute opacity-50 hover:opacity-100 cursor-pointer z-10 hidden group-hover:block'
          size={40}
        />
        <div
          id={'slider' + rowID}
          className='w-full h-full overflow-x-scroll whitespace-nowrap scroll-smooth scrollbar-hide relative'
        >
          {projects.map((item) => {
             if (item.rowID == parseInt(rowID,10)) {


              return <BookSlicer name={item.name} id ={item.id} desc={item.bio} />
             }
             return null
          })}
        </div>
        <MdChevronRight
          onClick={slideRight}
          className='bg-white right-0 rounded-full absolute opacity-50 hover:opacity-100 cursor-pointer z-10 hidden group-hover:block'
          size={40}
        />
      </div>
    </>
  );
};