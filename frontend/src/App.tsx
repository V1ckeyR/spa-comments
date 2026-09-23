import './App.css'
import { CommentTree } from './components/CommentTree'

import { LucideProvider } from 'lucide-react'

function App() {

  return (
    <LucideProvider size={16}>
      <div>
        <CommentTree />
      </div>
    </LucideProvider>
  )
}

export default App
