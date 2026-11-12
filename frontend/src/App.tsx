import './App.css'
import { CommentTree } from './components/CommentTree'

import { LucideProvider } from 'lucide-react'
import { useAuthContext } from './context/AuthContext';
import { Login } from './components/Login';
import { NavBar } from './components/NavBar';

function App() {
  const { token } = useAuthContext();

  if (!token) {
    return <Login />;
  }

  return (
    <LucideProvider size={16}>
      <div>
        <NavBar/>
        <CommentTree />
      </div>
    </LucideProvider>
  )
}

export default App
