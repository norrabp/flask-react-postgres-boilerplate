import React from 'react';
import Navbar from '@components/Navbar';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="min-vh-100 bg-dark text-light">
      <Navbar />
      <main className="container py-4">
        {children}
      </main>
    </div>
  );
};

export default Layout;
