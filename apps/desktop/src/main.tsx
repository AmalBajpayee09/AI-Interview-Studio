import React from 'react';
import {createRoot} from 'react-dom/client';
import App from './App';
import Overlay from './Overlay';
import './style.css';
const root=document.getElementById('root');if(root)createRoot(root).render(<React.StrictMode>{window.location.search.includes('workspace=1')?<App/>:<Overlay/>}</React.StrictMode>);
