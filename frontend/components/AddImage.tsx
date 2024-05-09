import "@styles/image-input.css";
import { motion } from "framer-motion";
import { useState, ChangeEvent, useEffect } from "react";

interface ProcessedImages {
  image: File;
  operation: string;
}

interface AddImageProps {
  onImageUpload: (
    data: { image: File; operation: string },
    index: number
  ) => void;
  processedImages: ProcessedImages[];
  index: number;
}

const AddImage = ({ onImageUpload, processedImages, index }: AddImageProps) => {
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [selectedOperation, setSelectedOperation] =
    useState<string>("color_inversion");

  const [ImageBeforeSrc, setImageBeforeSrc] = useState<string>(
    "/assets/placeholder.png"
  );
  const [ImageAfterSrc, setImageAfterSrc] = useState<string>(
    "/assets/placeholder.png"
  );

  useEffect(() => {
    if (imageFile && processedImages.length > 0) {
      processedImages.forEach((processedImage) => {
        if (processedImage.image.name === imageFile.name) {
          setImageAfterSrc(URL.createObjectURL(processedImage.image));
        }
      });
    }
  }, [imageFile, processedImages]);

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setImageFile(file);
      setImageBeforeSrc(URL.createObjectURL(file));
      onImageUpload({ image: file, operation: selectedOperation }, index);
    }
  };

  const handleOperationChange = (event: ChangeEvent<HTMLSelectElement>) => {
    setSelectedOperation(event.target.value);
    if (imageFile != null) {
      onImageUpload({ image: imageFile, operation: event.target.value }, index);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, x: -100 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -100 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
      className='flex justify-center items-center gap-12 mt-6 bg-white p-5 rounded-xl shadow-lg'
    >
      <div className='flex flex-col w-full gap-4 max-w-sm'>
        <input
          type='file'
          id='images'
          accept='image/*'
          required
          onChange={handleFileChange}
        />

        <select
          id='operations'
          className='bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-3 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
          value={selectedOperation}
          onChange={handleOperationChange}
        >
          <option value='edge_detection'>Edge Detection</option>
          <option value='color_inversion'>Color Inversion</option>
          <option value='grayscale'>Grayscale</option>
          <option value='blur'>Blur</option>
          <option value='thresholding'>Thresholding</option>
          <option value='dilation'>Dilation</option>
          <option value='erosion'>Erosion</option>
          <option value='opening'>Opening</option>
          <option value='closing'>Closing</option>
        </select>
      </div>

      <div className='flex justify-between items-center w-full '>
        <label className='text-center text-xl font-semibold'>
          Before
          <img
            src={ImageBeforeSrc}
            alt='image'
            className='rounded-lg shadow-lg object-cover w-96 img-before'
          />
        </label>

        <label className='text-center text-xl font-semibold'>
          After
          <img
            src={ImageAfterSrc}
            alt='image'
            className='rounded-lg shadow-lg object-cover w-96 img-after'
          />
        </label>
      </div>
    </motion.div>
  );
};

export default AddImage;
