import { motion } from "framer-motion"

const dotVariants = {
  initial: { y: 0 },
  animate: {
    y: -20,
    transition: {
      duration: 0.6,
      repeat: Infinity,
      repeatType: "mirror",
      ease: "easeInOut",
    },
  },
}

const containerVariants = {
  animate: {
    transition: {
      staggerChildren: 0.2,
      repeat: Infinity, // opcional si quieres que se repita el stagger
    },
  },
}

const Loader = () => {
  return (
    <div className="fixed inset-0 flex items-center justify-center bg-custom-brown-50 z-50">
      <motion.div
        className="flex gap-2"
        variants={containerVariants}
        initial="initial"
        animate="animate"
      >
        <motion.div
          className="w-5 h-5 rounded-full bg-custom-brown-600 will-change-transform"
          variants={dotVariants}
        />
        <motion.div
          className="w-5 h-5 rounded-full bg-custom-brown-600 will-change-transform"
          variants={dotVariants}
        />
        <motion.div
          className="w-5 h-5 rounded-full bg-custom-brown-600 will-change-transform"
          variants={dotVariants}
        />
      </motion.div>
    </div>
  )
}

export default Loader
