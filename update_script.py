import re

with open('d:/Users/clebe/Documentos/MEGA/BOT/treino/5-essenciais/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update the Pilares title to include Edit button and IDs
html = html.replace('<h2>🏆 Os 5 Pilares</h2>', '<h2 style="display:flex; justify-content:space-between; align-items:center; margin:0 0 10px 0;">🏆 Os 5 Pilares <button onclick="abrirConfig()" style="background:none; border:none; padding:4px; font-size:20px; cursor:pointer;" title="Editar Treinos">⚙️</button></h2>')
html = html.replace('<b>🦵 Agachamento</b><span>3×12</span>', '<b>🦵 Agachamento</b><span id="lbl-agachamento">3×12</span>')
html = html.replace('<b>💪 Flexão</b><span>3×10</span>', '<b>💪 Flexão</b><span id="lbl-flexao">3×10</span>')
html = html.replace('<b>🏋️ Remada</b><span>3×12/lado</span>', '<b>🏋️ Remada</b><span id="lbl-remada">3×12/lado</span>')
html = html.replace('<b>🧱 Prancha</b><span>3×40s</span>', '<b>🧱 Prancha</b><span id="lbl-prancha">3×40s</span>')
html = html.replace('<b>🚴 Bike HIIT</b><span>10x (30s Tiro / 60s Leve)</span>', '<b>🚴 Bike HIIT</b><span id="lbl-bike">10x (30s Tiro / 60s Leve)</span>')

# 2. Add Modal HTML before Backup Modal
modal_html = """
  <!-- Modal Config Treino -->
  <div id="modalConfigTreino" class="modal-overlay hidden">
    <div class="modal-card" style="max-height:80vh; overflow-y:auto; text-align:left;">
      <h2 style="margin-top:0; text-align:center;">⚙️ Configurar Treinos</h2>
      <div id="configFields"></div>
      <div class="modal-buttons" style="margin-top:20px;">
        <button class="btn-modal-cancel" onclick="fecharConfig()">Cancelar</button>
        <button class="btn-modal-ok" onclick="salvarConfig()">Salvar</button>
      </div>
    </div>
  </div>
"""
html = html.replace('  <!-- Backup Modal -->', modal_html + '  <!-- Backup Modal -->')

# 3. Add JS functions after let ultimoRelatorioTexto = "";
js_code = """
    function getSettings() {
      let def = {
        agachamento: { s: 3, r: 12, t: 40, d: 45 },
        flexao: { s: 3, r: 10, t: 40, d: 45 },
        remada: { s: 3, r: 12, t: 50, d: 45 },
        prancha: { s: 3, r: 40, t: 40, d: 40 },
        bike: { s: 10, t: 30, l: 60 }
      };
      let saved = JSON.parse(localStorage.getItem('workout_config') || '{}');
      for (let k in saved) { if (def[k]) Object.assign(def[k], saved[k]); }
      return def;
    }

    function abrirConfig() {
      let cfg = getSettings();
      let html = '';
      let exercises = {
        agachamento: '🦵 Agachamento', flexao: '💪 Flexão', 
        remada: '🏋️ Remada', prancha: '🧱 Prancha', bike: '🚴 Bike HIIT'
      };
      
      for(let k in exercises) {
        let c = cfg[k];
        html += `<div style="margin-bottom:15px; border-bottom:1px solid #e2e8f0; padding-bottom:10px;">
          <b>${exercises[k]}</b>
          <div class="row" style="margin-top:5px;">
            <input type="number" id="cfg_${k}_s" value="${c.s}" placeholder="Séries" title="Séries">
            ${k !== 'bike' ? `<input type="number" id="cfg_${k}_r" value="${c.r}" placeholder="Reps/s" title="Repetições">` : ''}
          </div>
          <div class="row" style="margin-top:5px;">
            <input type="number" id="cfg_${k}_t" value="${c.t}" placeholder="Trabalho (s)" title="Tempo de Trabalho (s)">
            <input type="number" id="cfg_${k}_${k==='bike'?'l':'d'}" value="${k==='bike'?c.l:c.d}" placeholder="Descanso (s)" title="Tempo de Descanso (s)">
          </div>
        </div>`;
      }
      document.getElementById('configFields').innerHTML = html;
      document.getElementById('modalConfigTreino').classList.remove('hidden');
    }

    function fecharConfig() { document.getElementById('modalConfigTreino').classList.add('hidden'); }

    function salvarConfig() {
      let cfg = getSettings();
      let exercises = ['agachamento', 'flexao', 'remada', 'prancha', 'bike'];
      for(let k of exercises) {
        cfg[k].s = +document.getElementById(`cfg_${k}_s`).value;
        cfg[k].t = +document.getElementById(`cfg_${k}_t`).value;
        if(k === 'bike') {
          cfg[k].l = +document.getElementById(`cfg_bike_l`).value;
        } else {
          cfg[k].r = +document.getElementById(`cfg_${k}_r`).value;
          cfg[k].d = +document.getElementById(`cfg_${k}_d`).value;
        }
      }
      localStorage.setItem('workout_config', JSON.stringify(cfg));
      fecharConfig();
      atualizarListaPilares();
      mostrarAviso('✅ Configurações salvas!');
    }

    function atualizarListaPilares() {
      let cfg = getSettings();
      let elAg = document.getElementById('lbl-agachamento'); if(elAg) elAg.textContent = `${cfg.agachamento.s}×${cfg.agachamento.r}`;
      let elFl = document.getElementById('lbl-flexao'); if(elFl) elFl.textContent = `${cfg.flexao.s}×${cfg.flexao.r}`;
      let elRe = document.getElementById('lbl-remada'); if(elRe) elRe.textContent = `${cfg.remada.s}×${cfg.remada.r}/lado`;
      let elPr = document.getElementById('lbl-prancha'); if(elPr) elPr.textContent = `${cfg.prancha.s}×${cfg.prancha.r}s`;
      let elBi = document.getElementById('lbl-bike'); if(elBi) elBi.textContent = `${cfg.bike.s}x (${cfg.bike.t}s Tiro / ${cfg.bike.l}s Leve)`;
    }
"""
html = html.replace('window.ultimoRelatorioTexto = "";', 'window.ultimoRelatorioTexto = "";\n' + js_code)

# 4. Update gerarBlocoBikeHIIT and add gerarBlocoForca and gerarBlocoUnico
old_bike_hiit = """    function gerarBlocoBikeHIIT() {
      let bloco = [['🚴 Bike — 5min Giro Leve (Aquec)', 300, true]];
      for (let i = 1; i <= 10; i++) {
        bloco.push([`⚡ BIKE TIRO PESADO! (${i}/10)`, 30, true]);
        bloco.push([`🚴 Bike Giro Leve (Recuperação ${i}/10)`, 60, true]);
      }
      bloco.push(['🧘 Bike — 5min Desacelerar', 300, true]);
      return bloco;
    }"""
new_bike_hiit = """    function gerarBlocoBikeHIIT() {
      let cfg = getSettings().bike;
      let bloco = [['🚴 Bike — 5min Giro Leve (Aquec)', 300, true]];
      for (let i = 1; i <= cfg.s; i++) {
        bloco.push([`⚡ BIKE TIRO PESADO! (${i}/${cfg.s})`, cfg.t, true]);
        bloco.push([`🚴 Bike Giro Leve (Recuperação ${i}/${cfg.s})`, cfg.l, true]);
      }
      bloco.push(['🧘 Bike — 5min Desacelerar', 300, true]);
      return bloco;
    }
    
    function gerarBlocoUnico(nome, c) {
      let b = [['Aquecimento geral', 180, false]];
      for(let i=1; i<=c.s; i++) {
        b.push([`${nome} - ${i}ª Série`, c.t, false]);
        if (i < c.s) b.push(['⏱️ Descanso', c.d, false]);
      }
      return b;
    }
    
    function gerarBlocoForca() {
      let cfg = getSettings();
      let b = [['Aquecimento geral', 180, false]];
      
      let pushExercise = (name, c) => {
        for(let i=1; i<=c.s; i++) {
          b.push([`${name} - ${i}ª Série`, c.t, false]);
          if (i < c.s) b.push(['⏱️ Descanso', c.d, false]);
        }
        b.push(['⏱️ Troca de Exercício', 60, false]);
      };
      
      pushExercise('Agachamento', cfg.agachamento);
      pushExercise('Flexão', cfg.flexao);
      pushExercise('Remada', cfg.remada);
      pushExercise('Prancha', cfg.prancha);
      
      return b;
    }"""
html = html.replace(old_bike_hiit, new_bike_hiit)

# 5. Remove blocoForca constant and replace plans
old_plans_block = re.search(r'const blocoForca = \[.*?\];.*?const plans = \{.*?6: \{.*?\}\s*    \};', html, re.DOTALL).group(0)
new_plans_block = """    const plans = {
      1: { name: '💪 SEG — Força + Bike HIIT (~49 min)', get items() { return [...gerarBlocoForca(), ...gerarBlocoBikeHIIT()] } },
      2: {
        name: '🚴 TER — Recuperação Ativa (~38 min)', items: [
          ['Aquecimento geral', 180, false],
          ['🚴 Bike LEVE 30min', 1800, false],
          ['🧘 Alongamento pernas/core', 300, false]
        ]
      },
      3: { name: '💪 QUA — Força + Bike HIIT (~49 min)', get items() { return [...gerarBlocoForca(), ...gerarBlocoBikeHIIT()] } },
      4: {
        name: '🚴 QUI — Recuperação Ativa (~38 min)', items: [
          ['Aquecimento geral', 180, false],
          ['🚴 Bike LEVE 30min', 1800, false],
          ['🧘 Alongamento + mobilidade', 300, false]
        ]
      },
      5: { name: '💪 SEX — Força + Bike HIIT (~49 min)', get items() { return [...gerarBlocoForca(), ...gerarBlocoBikeHIIT()] } },
      6: {
        name: '🚶 SÁB — Descanso Ativo (~40 min)', items: [
          ['🚶 Caminhada leve 25min', 1500, false],
          ['🧘 Alongamento geral 10min', 600, false]
        ]
      }
    };"""
html = html.replace(old_plans_block, new_plans_block)

# 6. Update startSingle()
old_startSingle = re.search(r'function startSingle\(type\) \{.*?load\(\);\n    \}', html, re.DOTALL).group(0)
new_startSingle = """function startSingle(type) {
      let cfg = getSettings();
      let bloco = [];
      if (type === 'agachamento') {
        bloco = gerarBlocoUnico('Agachamento', cfg.agachamento);
        currentTreinoName = 'Treino Avulso: Agachamento';
      } else if (type === 'flexao') {
        bloco = gerarBlocoUnico('Flexão', cfg.flexao);
        currentTreinoName = 'Treino Avulso: Flexão';
      } else if (type === 'remada') {
        bloco = gerarBlocoUnico('Remada', cfg.remada);
        currentTreinoName = 'Treino Avulso: Remada';
      } else if (type === 'prancha') {
        bloco = gerarBlocoUnico('Prancha', cfg.prancha);
        currentTreinoName = 'Treino Avulso: Prancha';
      } else if (type === 'bike') {
        bloco = gerarBlocoBikeHIIT();
        currentTreinoName = 'Treino Avulso: Bike HIIT';
      }
      
      solicitarWakeLock();
      items = bloco; idx = 0; tempoAcabou = false; show('guided'); load();
    }"""
html = html.replace(old_startSingle, new_startSingle)

# 7. Add atualizarListaPilares() to home()
html = html.replace('week.innerHTML = [1, 2, 3, 4, 5, 6, 0].map(d => `<div class="exercise ${d === day ? \'current\' : \'\'}"><div><b>${D[d]}</b><span>${plans[d]?.name || \'🛌 Descanso Total / Lazer\'}</span></div><span>${d === day ? \'👉\' : \'\'}</span></div>`).join(\'\');', 
'week.innerHTML = [1, 2, 3, 4, 5, 6, 0].map(d => `<div class="exercise ${d === day ? \'current\' : \'\'}"><div><b>${D[d]}</b><span>${plans[d]?.name || \'🛌 Descanso Total / Lazer\'}</span></div><span>${d === day ? \'👉\' : \'\'}</span></div>`).join(\'\');\n      atualizarListaPilares();')


with open('d:/Users/clebe/Documentos/MEGA/BOT/treino/5-essenciais/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Success')
