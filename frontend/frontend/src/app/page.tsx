"use client";
import { useState, useEffect } from "react";
import axios from "axios";

// Definisci il tipo per i corsi
type Corso = {
  id: number;
  titolo: string;
  link: string;
  domanda?: string;
  numero_corsi?: string;
  ricavo_medio?: string;
  ricavo_massimo?: string;
  percentuale_domanda_studenti?: string;
  percentuale_numero_corsi?: string;
};

export default function Home() {
  const [corsi, setCorsi] = useState<Corso[]>([]);
  const [titolo, setTitolo] = useState("");
  const [link, setLink] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [sortKey, setSortKey] = useState<keyof Corso | "">("");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("asc");

  useEffect(() => {
    fetchCorsi();
  }, [sortKey]);

  useEffect(() => {
    if (corsi.length > 0 && !sortKey) {
      setSortKey("ricavo_massimo");
      setSortOrder("desc");
    }
  }, [corsi, sortKey]); // ✅ ora è completo


  const fetchCorsi = () => {
    axios
      .get("http://127.0.0.1:8000/api/corsi")
      .then((response) => {
        console.log("Corsi ricevuti:", response.data);
        setCorsi(response.data);
      })
      .catch((error) => console.error("Errore nel recupero dei corsi", error));
  };

  const parseValue = (val: string) =>
    parseFloat(val.replace("US$", "").replace(/\./g, "").replace(",", "").trim()) || 0;

  const sortedCorsi = [...corsi].sort((a, b) => {
    if (!sortKey) return 0;

    const aVal = a[sortKey] ?? "";
    const bVal = b[sortKey] ?? "";

    // Ricavi: parsing da stringa con US$
    if (sortKey === "ricavo_massimo" || sortKey === "ricavo_medio") {
      return sortOrder === "asc"
        ? parseValue(aVal as string) - parseValue(bVal as string)
        : parseValue(bVal as string) - parseValue(aVal as string);
    }

    // ✅ ID: confronto numerico diretto
    if (sortKey === "id") {
      return sortOrder === "asc"
        ? (aVal as number) - (bVal as number)
        : (bVal as number) - (aVal as number);
    }

    // Tutti gli altri: confronto come stringa
    return sortOrder === "asc"
      ? String(aVal).localeCompare(String(bVal))
      : String(bVal).localeCompare(String(aVal));
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!titolo || !link) return alert("Compila tutti i campi");
    try {
      await axios.post("http://127.0.0.1:8000/api/corsi", { titolo, link });
      setTitolo("");
      setLink("");
      fetchCorsi();
    } catch (error) {
      console.error("Errore nell'aggiunta del corso", error);
    }
  };

  const deleteCorso = async (id: number) => {
    try {
      await axios.delete(`http://127.0.0.1:8000/api/corsi/${id}`);
      fetchCorsi();
    } catch (error) {
      console.error("Errore nella cancellazione", error);
    }
  };

  const startScraper = async () => {
    setIsLoading(true);
    try {
      const response = await axios.get("http://127.0.0.1:8000/api/scraper");
      alert(response.data.message || "Scraping completato con successo!");
      fetchCorsi();
    } catch (error) {
      console.error("Errore nell'avvio dello scraper", error);
    } finally {
      setIsLoading(false);
    }
  };

  const arricchisci = async (titolo: string) => {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/api/arricchisci/${titolo}`);
      alert(response.data.message || "Arricchimento completato con successo!");
      fetchCorsi();
    } catch (error) {
      console.error("Errore nell'arricchimento", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSort = (key: keyof Corso) => {
    if (sortKey === key) {
      setSortOrder(sortOrder === "asc" ? "desc" : "asc");
    } else {
      setSortKey(key);
      setSortOrder("asc");
    }
  };

  const getPercentColor = (value?: string) => {
    if (!value) return "text-gray-600";
    const num = parseInt(value);
    if (isNaN(num)) return "text-gray-600";
    if (num >= 70) return "text-green-600 font-semibold";
    if (num >= 40) return "text-yellow-600 font-medium";
    return "text-red-600";
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Corsi Udemy</h1>

      {isLoading && <p className="text-blue-500 mb-2">Caricamento in corso...</p>}

      <form onSubmit={handleSubmit} className="mb-4 space-y-2">
        <input type="text" placeholder="Titolo del corso" value={titolo} onChange={(e) => setTitolo(e.target.value)} className="border p-2 rounded w-full" />
        <input type="text" placeholder="Link al corso" value={link} onChange={(e) => setLink(e.target.value)} className="border p-2 rounded w-full" />
        <button type="submit" className="bg-blue-500 text-white p-2 rounded w-full">Aggiungi Corso</button>
      </form>

      <button onClick={startScraper} className={`bg-green-500 text-white p-2 rounded w-full ${isLoading ? "opacity-50" : ""}`} disabled={isLoading}>
        {isLoading ? "Esecuzione..." : "Avvia Scraper"}
      </button>

      <div className="flex flex-wrap gap-2 mb-4">
        <button onClick={() => handleSort("id" as keyof Corso)} className="bg-gray-200 p-1 rounded">
          ID {sortKey === "id" ? (sortOrder === "asc" ? "↑" : "↓") : ""}
        </button>
        <button onClick={() => handleSort("titolo" as keyof Corso)} className="bg-gray-200 p-1 rounded">
          Titolo {sortKey === "titolo" ? (sortOrder === "asc" ? "↑" : "↓") : ""}
        </button>
        <button onClick={() => handleSort("ricavo_massimo" as keyof Corso)} className="bg-gray-200 p-1 rounded">
          Ricavo Max {sortKey === "ricavo_massimo" ? (sortOrder === "asc" ? "↑" : "↓") : ""}
        </button>
        <button onClick={() => handleSort("domanda" as keyof Corso)} className="bg-gray-200 p-1 rounded">
          Domanda {sortKey === "domanda" ? (sortOrder === "asc" ? "↑" : "↓") : ""}
        </button>
      </div>

      <ul className="space-y-2">
        {corsi.length === 0 ? (
          <p>Nessun corso disponibile.</p>
        ) : (
          sortedCorsi.map((corso) => (
            <li key={corso.id} className="border p-3 rounded">
              <div className="flex justify-between items-center">
                <a href={corso.link} target="_blank" rel="noopener noreferrer" className="font-semibold text-blue-600">
                  {corso.id} - {corso.titolo}
                </a>
                <div className="flex space-x-2">
                  <button onClick={() => deleteCorso(corso.id)} className="bg-red-500 text-white px-2 py-1 rounded">
                    Elimina
                  </button>
                  <button onClick={() => arricchisci(corso.titolo)} className="bg-orange-500 text-white px-2 py-1 rounded">
                    Arricchisci
                  </button>
                </div>
              </div>

              <div className="col-span-3 border-t pt-3 text-sm text-gray-700 space-y-2">
                {/* Domanda */}
                <div>
                  <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                    <div><strong>Domanda:</strong> {corso.domanda || "—"}</div>
                    <div>
                      <strong>Percentuale Domanda:</strong>{" "}
                      <span className={getPercentColor(corso.percentuale_domanda_studenti)}>
                        {corso.percentuale_domanda_studenti ? `${corso.percentuale_domanda_studenti}%` : "—"}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Corsi */}
                <div>
                  <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                    <div><strong>Numero Corsi:</strong> {corso.numero_corsi || "—"}</div>
                    <div>
                      <strong>Percentuale Corsi:</strong>{" "}
                      <span className={getPercentColor(corso.percentuale_numero_corsi)}>
                        {corso.percentuale_numero_corsi ? `${corso.percentuale_numero_corsi}%` : "—"}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Ricavi */}
                <div>
                  <h3 className="font-semibold text-gray-800 border-b pb-1 mb-1">Ricavi</h3>
                  <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                    <div><strong>Ricavo Medio:</strong> {corso.ricavo_medio || "—"}</div>
                    <div><strong>Ricavo Max:</strong> {corso.ricavo_massimo || "—"}</div>
                  </div>
                </div>
              </div>


            </li>
          ))
        )}
      </ul>
    </div>
  );
}
