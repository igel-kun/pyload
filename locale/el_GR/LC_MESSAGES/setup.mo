��    l      |  �   �      0	     1	     C	     S	     `	     s	     �	     �	     �	     �	     �	     �	     �	     �	     
  m   	
  N   w
     �
  
   �
  B   �
     (     7     O  C   d  4   �  7   �       &   3  j   Z     �     �  J   �  Q   4     �     �  $   �  Q   �  8   #  @   \  q   �  B        R  H   `  	   �     �  a   �          0  -   G     u     �  ,   �  
   �     �  &   �          $     9     L     f     t     {  E   �     �     �  K     ;   _  :   �  5   �  T         a     �     �     �  E   �  z   �     a  .   n  /   �  A   �  ?     A   O  5   �  \   �  /   $  8   T  =   �     �  F   �     /     D     Z     \  U   b     �     �      �     �     �     
  K   !  I   m     �     �  G   �                 �    )   �           (  )   A  ;   k     �     �  <   �     �  !        <     W  8   u     �  �   �  �   �  Y   8  2   �  �   �     �  $   �  4   �  �   �  �   �   �   Y!  .   �!  C   "  �   R"  )   +#  H   U#  �   �#  �   c$  3   O%  0   �%  f   �%  �   &  c   �&  �   A'  �   �'  �   �(  %   ,)  �   R)     �)     �)  �   *  5   �*  C    +  �   D+     �+  �   �+  �   �,     
-  /   '-  i   W-     �-  '   �-     �-  K   .  !   X.     z.  Q   �.  �   �.  I   }/  6   �/  �   �/  �   �0  �   ;1  d   �1  �   >2  H   �2  &    3     G3     _3  �   n3  D  4     Z5  I   t5  p   �5  �   /6  c   �6  v   ;7  q   �7  �   $8  s   �8  �   29  �   �9  9   :  N   �:  9   ;     B;     X;  
   Z;  �   e;     <     <  E   <  -   [<  -   �<  3   �<  �   �<  �   �=     .>     A>  x   C>  
   �>     �>     �>     `      "   -       =   R   a       (   ?   G   9          ^   j                      F           P          J   )   0   M   f      #   1   %   X   c   +   V   O   ,       Q                            b   5   /   <       W   2      *       i      
   [   ;       D                       l                 8       I   h   e           E           3   C       g                     H      \              .      @   $   _   T   >           U      ]       L   '   &   A       !          7   6   K                    k   S   Y      d          :   Z   B   	   4   N        ## Basic Setup ## ## SSL Setup ## ## Status ## ## System Check ## ## Webinterface Setup ## %s: OK %s: missing 1 - Create/Edit user 2 - List users 3 - Remove user 4 - Quit Activate SSL? Activate webinterface? Address Attention: In some rare cases the builtin server is not working, if you notice problems with the webinterface Can be used by apache, lighttpd, etc.; needs to be properly configured before. Change config path? Configpath Configpath changed, setup will now close, please restart to go on. Configure ssl? Configure webinterface? Continue with setup? Default server; best choice if you plan to use pyLoad just for you. Do you want to change the config path? Current is %s Do you want to configure login data and basic settings? Do you want to configure ssl? Do you want to configure webinterface? Don't forget: You can always rerun this assistant with --setup or -s parameter, when you start pyLoadCore. Downloadfolder Enable remote access Execute these commands from pyLoad config folder to make ssl certificates: External clients (GUI, CLI or other) need remote access to work over the network. Featues missing:  Features available: Hit enter to exit and restart pyLoad However, if you only want to use the webinterface you may disable it to save ram. If you have any problems with this assistant hit STRG-C, If you only want to access locally to pyLoad ssl is not usefull. If you use pyLoad on a server or the home partition lives on an iternal flash it may be a good idea to change it. If you're done and everything went fine, you can activate ssl now. Invalid Input It will check your system and make a basic setup in order to run pyLoad. JS engine Language Listen address, if you use 127.0.0.1 or localhost, the webinterface will only accessible locally. Make basic setup? Max parallel downloads Only needed for some hosters and as freeuser. Password (again):  Password must be alphanumeric. Password too short! Use at least %s symbols. Password:  Passwords did not match. Please correct this and re-run pyLoad. Port Press Enter to exit. Python Version: OK Reconnect script location Select action Server Setting config path failed: %s Setting new configpath, current configuration will not be transfered! Setup finished successfully. Setup will now close. Support SSL connection and can serve simultaneously more client flawlessly. System check finished, hit enter to see your status report. The following logindata is valid for CLI and webinterface. The value in brackets [] always is the default value, This is needed if you want to establish a secure connection to core or webinterface. This is recommend for first run. Use Reconnect? Username Users Very fast alternative to builtin; requires libev and bjoern packages. Warning: Consider a password of 10 or more symbols if you expect to access from outside your local network (ex. internet). Webinterface Welcome to the pyLoad Configuration Assistant. When you are ready for system check, hit enter. You can abort the setup now and fix some dependicies if you want. You can safely continue but if the webinterface is not working, You need pycurl, sqlite and python 2.5, 2.6 or 2.7 to run pyLoad. You need this if you want to decrypt container files. You will need this for some Click'N'Load links. Install Spidermonkey, ossp-js, pyv8 or rhino Your installed jinja2 version %s seems too old. Your python version is to new, Please use Python 2.6/2.7 Your python version is to old, Please use at least Python 2.5 automatic captcha decryption come back here and change the builtin server to the threaded one here. container decrypting extended Click'N'Load f false in case you don't want to change it or you are unsure what to choose, just hit enter. n no no Captcha Recognition available no JavaScript engine found no SSL available no py-crypto available please upgrade or deinstall it, pyLoad includes a sufficient jinja2 libary. pyLoad offers several server backends, now following a short explanation. ssl connection t to abort and don't let him start with pyLoadCore automatically anymore. true y yes Project-Id-Version: pyload
Report-Msgid-Bugs-To: 'bugs@pyload.net'
POT-Creation-Date: 2014-07-13 20:53+0200
PO-Revision-Date: 2015-01-18 18:30-0500
Last-Translator: pyloadTeam <team@pyload.net>
Language-Team: Greek
Language: el_GR
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=2; plural=(n != 1);
X-Generator: crowdin.com
X-Crowdin-Project: pyload
X-Crowdin-File: /pyLoad/setup.pot
 ## Βασική Εγκατάσταση ## ## Εγκατάσταση SSL ## ## Κατάσταση ## ## Έλεγχος Συστήματος ## ## Εγκατάσταση Περιβάλλοντος Web ## %s: OK %s: λείπει 1 - Δημιουργία/Επεξεργασία χρήστη 2 - Λίστα χρηστών 3 - Διαγραφή χρήστη 4 - Τερματισμός Ενεργοποίηση SSL; Ενεργοποίηση περιβάλλοντος Web; Διεύθυνση Προσοχή: Σε σπάνιες περιπτώσεις ο προεπιλεγμένος διακομιστής δεν δουλεύει. Αν παρατηρήσετε προβλήματα με το Web Interface, Μπορεί να χρησιμοποιηθεί από τον apache, τον lighttpd, κλπ· πρέπει να ρυθμιστεί σωστά από πριν. Αλλαγή διαδρομής αποθήκευσης αρχείου ρυθμίσεων; Διαδρομή αρχείου ρυθμίσεων Η διαδρομή ρυθμίσεων ορίστηκε, η εγκατάσταση τώρα θα κλείσει, παρακαλώ κάντε επανεκκίνηση για να συνεχίστε. Ρύθμιση SSL; Ρύθμιση του Web Interface; Συνέχιση με την εγκατάσταση; Προεπιλεγμένος διακομιστής· η καλύτερη επιλογή εάν σκοπεύετε να χρησιμοποιήσετε το pyLoad μόνο για εσάς. Θέλετε να αλλάξετε τη διαδρομή του αρχείου αποθήκευσης των ρυθμίσεων; Η τρέχουσα είναι %s Θέλετε να ορίσετε στοιχεία σύνδεσης και να κάνετε τις βασικές ρυθμίσεις; Θέλετε να ρυθμίσετε το SSL; Θέλετε να ρυθμίσετε το περιβάλλον Web; Μην ξεχνάτε: Μπορείτε πάντα να εκτελέσετε ξανά τον Βοηθό, εισάγοντας τη παράμετρο --setup ή -s, κατά την εκτέλεση του pyLoadCore. Φάκελος μεταφορτώσεων Ενεργοποίηση απομακρυσμένης πρόσβασης Εκτελέστε αυτές τις εντολές από τον φάκελο παραμετροποίησης του pyLoad για να δημιουργήσετε πιστοποιητικά SSL: Οι εξωτερικοί πελάτες (για το GUI, τη Γραμμή εντολών ή άλλο) χρειάζονται απομακρυσμένη πρόσβαση για να λειτουργήσουν μέσω δικτύου. Χαρακτηριστικά που λείπουν: Χαρακτηριστικά διαθέσιμα: Πατήστε Enter για να εξέλθετε και να επανεκκινήσετε το pyLoad Όμως, αν θέλετε να να χρησιμοποιήσετε μονο το Web Interface, μπορείτε να το απενεργοποιήσετε για να γλυτώσετε RAM. Αν αντιμετωπίσετε προβλήματα με το Βοηθό, πατήστε CTRL-C, Αν θέλετε να έχετε πρόσβαση μόνο τοπικά στο pyLoad, το ssl δεν είναι χρήσιμο. Αν χρησιμοποιήτε το pyLoad σε εξυπηρετητή ή το διαμέρισμα home βρίσκεται σε εσωτερική μνήμη flash, θα ήταν καλή ιδέα να το αλλάξετε. Αν τελειώσατε και όλα πήγαν καλώς, τώρα μπορείτε να ενεργοποιήσετε το SSL. Λανθασμένη εισαγωγή Θα γίνει έλεγχος και βασική ρύθμιση του συστήματός σας, ώστε να εκτελεστεί το pyLoad. Μηχανή JS Γλώσσα Διεύθυνση που θα "ακούει". Αν χρησιμοποιήσετε 127.0.0.1 ή localhost, το περιβάλλον Web θα είναι προσβάσιμο μόνο τοπικά. Δημιουργία βασικής ρύθμισης; Μέγιστος αριθμός ταυτόχρονων λήψεων Χρειάζεται μόνο από μερικούς διακομιστές διαμοιρασμού αρχείων και σαν δωρεάν χρήστης. Κωδικός (ξανά): Ο κωδικός πρόσβασης πρέπει να αποτελείται από αλφαριθμητικούς χαρακτήρες. Ο κωδικός είναι πολύ μικρός! Χρησιμοποιήστε τουλάχιστον %s χαρακτήρες. Κωδικός χρήστη: Οι κωδικοί δεν ταιριάζουν Παρακαλώ κάνετε τις διορθώσεις και εκτελέστε ξανά το pyLoad. Θύρα Πατήστε Enter για έξοδο. Έκδοση Python: ΟΚ Τοποθεσία αρχείου εντολών επανασύνδεσης Επιλέξτε ενέργεια Διακομιστής Ο ορισμός της διαδρομής ρυθμίσεων απέτυχε: %s Ορισμός καινούριας διαδρομής ρυθμίσεων, δεν θα μεταφερθούν οι τρέχουσες ρυθμίσεις! Η εγκατάσταση ολοκληρώθηκε με επιτυχία. Η εγκατάσταση θα τερματιστεί. Υποστηρίζει σύνδεση SSL και μπορεί να εξυπηρετήσει καλύτερα πολλούς ταυτόχρονους πελάτες. Ο έλεγχος του συστήματος ολοκληρώθηκε, πατήστε το enter για να δείτε τα αποτελέσματα. Τα ακόλουθα στοιχεία σύνδεσης είναι έγκυρα για τη Γραμμή Εντολών και το περιβάλλον Web. Η τιμή στις αγκύλες [] είναι πάντα η προεπιλεγμένη τιμή, Αυτό απαιτείται για την πραγματοποίηση ασφαλής σύνδεσης με τον πυρήνα ή το Webιnterface. Αυτό συνιστάται για την πρώτη εκτέλεση. Χρήση Επανασύνδεσης; Όνομα Χρήστη Χρήστες Πολύ γρήγορη εναλλακτική λύση του ενσωματωμένου διακομιστή· απαιτεί τα πακέτα libev και bjoern. Προσοχή: Προτείνεται η χρήση κωδικού πρόσβασης αποτελούμενου από 10 ή περισσότερους χαρακτήρες  εάν σκοπεύετε να έχετε πρόσβαση από έξω από το τοπικό σας δίκτυο (π.χ. από το internet). Διεπαφή ιστού Καλώς ήλθατε στο Βοηθό Ρύθμισης του pyLoad. Όταν είστε έτοιμος για τον έλεγχο του συστήματος, πατήστε enter. Αν θέλετε μπορείτε να ακυρώσετε την εγκατάσταση τώρα και να διορθώσετε κάποιες εξαρτήσεις. Μπορείτε να συνεχίστε, αλλά αν δεν δουλεύει το Web Interface, Απαιτούνται τα pycurl, sqlite και python 2.5, 2.6 ή 2.7 για να εκτελέσετε το pyLoad. Αυτό απαιτείται αν θέλετε να αποκρυπτογραφήσετε αρχεία container. Θα το χρειαστείτε για μερικούς συνδέσμους Click'N'Load. Εγκαταστήστε Spidermonkey, ossp-js, pyv8 ή rhino Η έκδοση %s του jinja2 που έχετε εγκατεστημένη φαίνεται πολύ παλιά. Η έκδοση της python που χρησιμοποιείτε είναι πολύ νέα, παρακαλώ χρησιμοποιήστε Python 2.6/2.7 Η έκδοση της python που χρησιμοποιείτε είναι πολύ παλιά, παρακαλώ χρησιμοποιήστε τουλάχιστον Python 2.5 αυτόματη αποκρυπτογράφηση captcha επιστρέψτε εδώ και αλλάξτε τον με τον threaded. αποκρυπτογράφηση περιεχόμενου extended Click'N'Load f λάθος σε περίπτωση που δεν επιθυμείτε αλλαγή ή αμφιβάλλετε για την επιλογή σας, απλά πατήστε enter.  n όχι δεν υπάρχει διαθέσιμη αναγνώριση Captcha δεν βρέθηκε μηχανή JavaScript δεν είναι διαθέσιμο το SSL δεν είναι διαθέσιμο το py-crypto παρακαλώ αναβαθμίστε το ή απεγκαταστήστε το, το pyLoad συμπεριλαμβάνει μια επαρκή βιβλιοθήκη jinja2. Το pyLoad προσφέρει αρκετoύς διακομιστές υποστήριξης. Ακολουθεί σύντομη επεξήγηση. σύνδεση ssl t για να εγκαταλείψετε και να αποτρέψετε την αυτόματη εκτέλεσή του. σωστό y ναι 