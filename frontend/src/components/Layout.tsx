import { ReactNode } from 'react';
import { Link } from 'react-router-dom';

export function Layout({ children }: { children: ReactNode }) {
  return (
    <>
      <header>
        <h1>Coletivo Piaya Cayana</h1>
        <nav>
          <Link to="/">Início</Link>
          <Link to="/agenda">Agenda</Link>
          <Link to="/galeria">Galeria</Link>
          <Link to="/artigos">Artigos</Link>
          <Link to="/sobre">Sobre</Link>
          <Link to="/contato">Contato</Link>
        </nav>
      </header>
      <main>{children}</main>
    </>
  );
}
