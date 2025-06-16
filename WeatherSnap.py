import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Index from "./pages/Index";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Index />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
import WeatherApp from '@/components/WeatherApp';

const Index = () => {
  return <WeatherApp />;
};

export default Index;
import React, { useState } from 'react';
import { Search, MapPin } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import WeatherDisplay from './WeatherDisplay';
import LoadingSpinner from './LoadingSpinner';
import { useToast } from '@/hooks/use-toast';

const API_KEY = 'ccb80a468f5f5c1d1fad547be31d46b4'; // OpenWeatherMap API key
const API_URL = 'https://api.openweathermap.org/data/2.5/weather';

interface WeatherData {
  name: string;
  main: {
    temp: number;
    feels_like: number;
    humidity: number;
  };
  weather: Array<{
    main: string;
    description: string;
    icon: string;
  }>;
  wind: {
    speed: number;
  };
  sys: {
    country: string;
  };
}
const WeatherApp = () => {
  const [city, setCity] = useState('');
  const [weatherData, setWeatherData] = useState<WeatherData | null>(null);
  const [loading, setLoading] = useState(false);
  const [backgroundClass, setBackgroundClass] = useState('bg-default-gradient');
  const { toast } = useToast();

  const getBackgroundClass = (weatherMain: string) => {
    const weather = weatherMain.toLowerCase();
    if (weather.includes('clear') || weather.includes('sun')) {
      return 'bg-sunny-gradient';
    } else if (weather.includes('cloud')) {
      return 'bg-cloudy-gradient';
    } else if (weather.includes('rain') || weather.includes('drizzle')) {
      return 'bg-rainy-gradient';
    } else if (weather.includes('snow')) {
      return 'bg-snowy-gradient';
    }
    return 'bg-default-gradient';
  };

  const fetchWeather = async (cityName: string) => {
    if (!cityName.trim()) {
      toast({
        title: "Please enter a city name",
        variant: "destructive",
      });
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(
        `${API_URL}?q=${cityName}&appid=${API_KEY}&units=metric`
      );
      
      if (!response.ok) {
        throw new Error('City not found');
      }
      
      const data: WeatherData = await response.json();
      setWeatherData(data);
      setBackgroundClass(getBackgroundClass(data.weather[0].main));
      
      toast({
        title: "Weather updated!",
        description: `Showing weather for ${data.name}`,
      });
    } catch (error) {
      toast({
        title: "Error fetching weather",
        description: "Please check the city name and try again",
        variant: "destructive",
      });
      console.error('Error fetching weather:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    fetchWeather(city);
  };

  const getCurrentLocation = () => {
    if (!navigator.geolocation) {
      toast({
        title: "Geolocation not supported",
        description: "Please enter a city manually",
        variant: "destructive",
      });
      return;
    }

    setLoading(true);
    navigator.geolocation.getCurrentPosition(
      async (position) => {
        try {
          const { latitude, longitude } = position.coords;
          const response = await fetch(
            `${API_URL}?lat=${latitude}&lon=${longitude}&appid=${API_KEY}&units=metric`
          );
          
          if (!response.ok) {
            throw new Error('Location weather not found');
          }
          
          const data: WeatherData = await response.json();
          setWeatherData(data);
          setCity(data.name);
          setBackgroundClass(getBackgroundClass(data.weather[0].main));
          
          toast({
            title: "Location detected!",
            description: `Showing weather for ${data.name}`,
          });
        } catch (error) {
          toast({
            title: "Error getting location weather",
            description: "Please try searching manually",
            variant: "destructive",
          });
        } finally {
          setLoading(false);
        }
      },
      () => {
        setLoading(false);
        toast({
          title: "Location access denied",
          description: "Please enter a city manually",
          variant: "destructive",
        });
      }
    );
  };

  return (
    <div className={`min-h-screen transition-all duration-1000 ${backgroundClass} flex items-center justify-center p-4 relative overflow-hidden`}>
      {/* Sun background image with glow effect */}
      <div 
        className="absolute inset-0 bg-cover bg-center bg-no-repeat opacity-30"
        style={{
          backgroundImage: `url('https://images.unsplash.com/photo-1469474968028-56623f02e42e?ixlib=rb-4.0.3&auto=format&fit=crop&w=3506&q=80')`,
          filter: 'brightness(1.2) contrast(1.1)'
        }}
      />
      
      {/* Radial glow overlay */}
      <div 
        className="absolute inset-0"
        style={{
          background: 'radial-gradient(circle at center, rgba(255, 215, 0, 0.3) 0%, rgba(255, 140, 0, 0.2) 30%, rgba(255, 69, 0, 0.1) 60%, transparent 100%)'
        }}
      />
      
      <div className="w-full max-w-md mx-auto space-y-6 relative z-10">
        <div className="text-center animate-fade-in">
          <h1 className="text-4xl font-bold text-white mb-2 drop-shadow-lg">
            WeatherSnap
          </h1>
          <p className="text-white/80 text-lg">
            Instant weather for any city
          </p>
        </div>

        <Card className="backdrop-blur-md bg-white/20 border-white/30 shadow-xl animate-fade-in">
          <CardContent className="p-6">
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-white/60 h-4 w-4" />
                <Input
                  type="text"
                  placeholder="Enter city name..."
                  value={city}
                  onChange={(e) => setCity(e.target.value)}
                  className="pl-10 bg-white/10 border-white/30 text-white placeholder:text-white/60 focus:bg-white/20 transition-all duration-200"
                />
              </div>
              
              <div className="flex gap-2">
                <Button 
                  type="submit" 
                  disabled={loading}
                  className="flex-1 bg-white/20 hover:bg-white/30 text-white border-white/30 transition-all duration-200"
                >
                  {loading ? 'Searching...' : 'Search'}
                </Button>
                
                <Button
                  type="button"
                  onClick={getCurrentLocation}
                  disabled={loading}
                  className="bg-white/20 hover:bg-white/30 text-white border-white/30 transition-all duration-200"
                  size="icon"
                >
                  <MapPin className="h-4 w-4" />
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>

        {loading && <LoadingSpinner />}
        
        {weatherData && !loading && <WeatherDisplay data={weatherData} />}
      </div>
    </div>
  );
};

export default WeatherApp;
import React from 'react';
import { 
  Cloud, 
  CloudRain, 
  CloudSnow, 
  Sun, 
  CloudDrizzle, 
  Thermometer,
  Wind
} from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';

interface WeatherData {
  name: string;
  main: {
    temp: number;
    feels_like: number;
    humidity: number;
  };
  weather: Array<{
    main: string;
    description: string;
    icon: string;
  }>;
  wind: {
    speed: number;
  };
  sys: {
    country: string;
  };
}

interface WeatherDisplayProps {
  data: WeatherData;
}

const WeatherDisplay: React.FC<WeatherDisplayProps> = ({ data }) => {
  const getWeatherIcon = (weatherMain: string, size: number = 64) => {
    const weather = weatherMain.toLowerCase();
    const iconProps = { size, className: "animate-bounce-subtle" };
    
    if (weather.includes('clear') || weather.includes('sun')) {
      return <Sun {...iconProps} className="text-yellow-300 animate-bounce-subtle" />;
    } else if (weather.includes('cloud')) {
      return <Cloud {...iconProps} className="text-gray-200 animate-bounce-subtle" />;
    } else if (weather.includes('rain')) {
      return <CloudRain {...iconProps} className="text-blue-200 animate-bounce-subtle" />;
    } else if (weather.includes('drizzle')) {
      return <CloudDrizzle {...iconProps} className="text-blue-300 animate-bounce-subtle" />;
    } else if (weather.includes('snow')) {
      return <CloudSnow {...iconProps} className="text-white animate-bounce-subtle" />;
    }
    return <Cloud {...iconProps} className="text-gray-200 animate-bounce-subtle" />;
  };

  const formatTemperature = (temp: number) => {
    return Math.round(temp);
  };

  return (
    <Card className="backdrop-blur-md bg-white/20 border-white/30 shadow-xl animate-fade-in">
      <CardContent className="p-6">
        <div className="text-center space-y-4">
          {/* Location */}
          <div>
            <h2 className="text-2xl font-bold text-white">
              {data.name}
            </h2>
            <p className="text-white/80">
              {data.sys.country}
            </p>
          </div>

          {/* Weather Icon */}
          <div className="flex justify-center">
            {getWeatherIcon(data.weather[0].main)}
          </div>

          {/* Temperature */}
          <div>
            <div className="text-5xl font-bold text-white mb-2">
              {formatTemperature(data.main.temp)}°C
            </div>
            <p className="text-white/80 text-lg capitalize">
              {data.weather[0].description}
            </p>
          </div>

          {/* Additional Info */}
          <div className="grid grid-cols-3 gap-4 pt-4 border-t border-white/20">
            <div className="text-center">
              <Thermometer className="h-5 w-5 text-white/80 mx-auto mb-1" />
              <p className="text-sm text-white/60">Feels like</p>
              <p className="text-white font-semibold">
                {formatTemperature(data.main.feels_like)}°C
              </p>
            </div>
            
            <div className="text-center">
              <div className="h-5 w-5 mx-auto mb-1 bg-white/80 rounded-full opacity-80"></div>
              <p className="text-sm text-white/60">Humidity</p>
              <p className="text-white font-semibold">
                {data.main.humidity}%
              </p>
            </div>
            
            <div className="text-center">
              <Wind className="h-5 w-5 text-white/80 mx-auto mb-1" />
              <p className="text-sm text-white/60">Wind</p>
              <p className="text-white font-semibold">
                {Math.round(data.wind.speed)} m/s
              </p>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default WeatherDisplay;
import React from 'react';
import { Card, CardContent } from '@/components/ui/card';

const LoadingSpinner = () => {
  return (
    <Card className="backdrop-blur-md bg-white/20 border-white/30 shadow-xl animate-fade-in">
      <CardContent className="p-6">
        <div className="text-center space-y-4">
          <div className="flex justify-center">
            <div className="animate-spin rounded-full h-16 w-16 border-4 border-white/30 border-t-white"></div>
          </div>
          <p className="text-white/80 text-lg">
            Getting weather data...
          </p>
        </div>
      </CardContent>
    </Card>
  );
};

export default LoadingSpinner;
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;
    --radius: 0.5rem;
  }

  * {
    @apply border-border;
  }

  body {
    @apply bg-background text-foreground;
  }
}
import type { Config } from "tailwindcss";

export default {
  darkMode: ["class"],
  content: [
    "./pages/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./app/**/*.{ts,tsx}",
    "./src/**/*.{ts,tsx}",
  ],
  prefix: "",
  theme: {
    container: {
      center: true,
      padding: '2rem',
      screens: {
        '2xl': '1400px'
      }
    },
    extend: {
      colors: {
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        primary: {
          DEFAULT: 'hsl(var(--primary))',
          foreground: 'hsl(var(--primary-foreground))'
        },
        secondary: {
          DEFAULT: 'hsl(var(--secondary))',
          foreground: 'hsl(var(--secondary-foreground))'
        },
        destructive: {
          DEFAULT: 'hsl(var(--destructive))',
          foreground: 'hsl(var(--destructive-foreground))'
        },
        muted: {
          DEFAULT: 'hsl(var(--muted))',
          foreground: 'hsl(var(--muted-foreground))'
        },
        accent: {
          DEFAULT: 'hsl(var(--accent))',
          foreground: 'hsl(var(--accent-foreground))'
        },
        popover: {
          DEFAULT: 'hsl(var(--popover))',
          foreground: 'hsl(var(--popover-foreground))'
        },
        card: {
          DEFAULT: 'hsl(var(--card))',
          foreground: 'hsl(var(--card-foreground))'
        }
      },
      backgroundImage: {
        'sunny-gradient': 'linear-gradient(135deg, #FFD700 0%, #FF8C00 100%)',
        'cloudy-gradient': 'linear-gradient(135deg, #87CEEB 0%, #B0C4DE 100%)',
        'rainy-gradient': 'linear-gradient(135deg, #4682B4 0%, #2F4F4F 100%)',
        'snowy-gradient': 'linear-gradient(135deg, #F0F8FF 0%, #E6E6FA 100%)',
        'default-gradient': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
      },
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)'
      },
      keyframes: {
        'accordion-down': {
          from: { height: '0' },
          to: { height: 'var(--radix-accordion-content-height)' }
        },
        'accordion-up': {
          from: { height: 'var(--radix-accordion-content-height)' },
          to: { height: '0' }
        },
        'fade-in': {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' }
        },
        'bounce-subtle': {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-5px)' }
        }
      },
      animation: {
        'accordion-down': 'accordion-down 0.2s ease-out',
        'accordion-up': 'accordion-up 0.2s ease-out',
        'fade-in': 'fade-in 0.5s ease-out',
        'bounce-subtle': 'bounce-subtle 2s ease-in-out infinite'
      }
    }
  },
  plugins: [require("tailwindcss-animate")],
} satisfies Config;
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>WeatherSnap - Instant Weather for Any City</title>
    <meta name="description" content="Get instant weather updates for any city with WeatherSnap. Clean, fast, and beautiful weather app." />
    <meta name="author" content="Lovable" />

    <meta property="og:title" content="WeatherSnap - Instant Weather for Any City" />
    <meta property="og:description" content="Get instant weather updates for any city with WeatherSnap. Clean, fast, and beautiful weather app." />
    <meta property="og:type" content="website" />
    <meta property="og:image" content="https://lovable.dev/opengraph-image-p98pqg.png" />

    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@lovable_dev" />
    <meta name="twitter:image" content="https://lovable.dev/opengraph-image-p98pqg.png" />
  </head>

  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
import { createRoot } from 'react-dom/client'
import App from './App.tsx'
import './index.css'

createRoot(document.getElementById("root")!).render(<App />);