import React, { useState, useEffect } from "react";
import { NavLink, useLocation } from "react-router-dom";
import { Sun, Moon, Menu, X, Sparkle } from "lucide-react";

const Navbar = () => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const location = useLocation();

  const pathSegments = location.pathname.split("/");
  const isUserRoute = ["rating", "recommended", "dashboard"].includes(pathSegments[1]);
  const extractedUser = isUserRoute && pathSegments.length > 2 ? pathSegments[2] : "";

  const [currentUsername, setCurrentUsername] = useState(() => localStorage.getItem("lastUsername") || "");

  useEffect(() => {
    if (extractedUser) {
      setCurrentUsername(extractedUser);
      localStorage.setItem("lastUsername", extractedUser);
    }
  }, [extractedUser]);

  const NAV_LINKS = [
    { name: "Dashboard", path: currentUsername ? `/dashboard/${currentUsername}` : "/home" },
    { name: "Rating Graph", path: currentUsername ? `/rating/${currentUsername}` : "/home" },
    { name: "Recommended", path: currentUsername ? `/recommended/${currentUsername}` : "/home" },
    { name: "AI Chat", path: currentUsername ? `/ai-chat/${currentUsername}` : "/home" },
  ];


  useEffect(() => {
    setMobileOpen(false); 
  }, [location.pathname]);

  return (
    <nav
      className="sticky top-0 z-50 w-full px-6 py-3 flex items-center justify-between rounded-b-xl shadow-sm bg-white/80 backdrop-blur-md text-black transition-all duration-300"
    >
      {/* Left: Logo */}
      <NavLink
        to="/home"
        className="font-extrabold text-lg tracking-wide select-none cursor-pointer"
      >
        CF ANALYZER
      </NavLink>

      {/* Center: Nav Links (Desktop) */}
      <div className="hidden md:flex gap-2 lg:gap-6 mx-4 flex-1 justify-center">
        {NAV_LINKS.map((link) => (
          <NavLink
            key={link.name}
            to={link.path}
            className={({ isActive }) =>
              `relative px-3 py-2 rounded-lg font-medium transition-all duration-300
              hover:bg-blue-100/30
              ${isActive
                ? "text-blue-600 after:absolute after:left-0 after:right-0 after:-bottom-1 after:h-0.5 after:bg-blue-500 after:rounded-full after:shadow-[0_0_8px_2px_rgba(59,130,246,0.5)]"
                : "text-gray-700"
              }`
            }
          >
            {link.name}
          </NavLink>
        ))}
      </div>

      {/* Right: Actions */}
      <div className="flex items-center gap-2 lg:gap-4">
        {/* AI Chat Button */}
        <NavLink
          // to="/ai-chat"
          to={currentUsername ? `/ai-chat/${currentUsername}` : "/home"}
          className={({ isActive }) =>
            `hidden sm:flex items-center gap-2 px-6 py-3 rounded-lg font-semibold shadow-sm
            transition-all duration-300
            bg-blue-600 hover:bg-blue-700 text-white
            ${isActive
              ? "ring-2 ring-blue-400 ring-offset-2"
              : ""
            }`
          }
        >
          <Sparkle className="w-5 h-5" />
          AI Chat
        </NavLink>
        {/* Hamburger (Mobile) */}
        <button
          className="md:hidden p-2 rounded-full hover:bg-gray-100 transition-all duration-300"
          onClick={() => setMobileOpen((v) => !v)}
          aria-label="Toggle Menu"
        >
          {mobileOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
        </button>
      </div>

      {/* Mobile Menu */}
      {mobileOpen && (
        <div className="fixed inset-0 top-16 z-40 bg-black/40 backdrop-blur-sm md:hidden">
          <div className="absolute right-4 top-4 bg-white rounded-xl shadow-lg p-6 flex flex-col gap-4 min-w-[60vw]">
            {NAV_LINKS.map((link) => (
              <NavLink
                key={link.name}
                to={link.path}
                className={({ isActive }) =>
                  `px-4 py-2 rounded-lg font-medium transition-all duration-300
                  hover:bg-blue-100/30
                  ${isActive
                    ? "text-blue-600 underline underline-offset-4"
                    : "text-gray-700"
                  }`
                }
              >
                {link.name}
              </NavLink>
            ))}
            <NavLink
              to={currentUsername ? `/ai-chat/${currentUsername}` : "/home"}
              className={({ isActive }) =>
                `hidden sm:flex items-center gap-2 px-6 py-3 rounded-lg font-semibold shadow-sm
    transition-all duration-300
    bg-blue-600 hover:bg-blue-700 text-white
    ${isActive
                  ? "ring-2 ring-blue-400 ring-offset-2"
                  : ""
                }`
              }
            >
              <Sparkle className="w-5 h-5" />
              AI Chat
            </NavLink>
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
